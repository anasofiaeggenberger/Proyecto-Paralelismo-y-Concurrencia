from PIL import Image, ImageOps, ImageFilter, ImageEnhance
from pika_banner import print_pikachu
from tqdm import tqdm
import requests
import time
import os
import concurrent.futures


def download_one(i, base_url, dir_name):
    file_name = f'{i:03d}.png'
    url = f'{base_url}/{file_name}'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img_path = os.path.join(dir_name, file_name)
        with open(img_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        return f'Error {file_name}: {e}'


def download_pokemon_concurrent(n=150, dir_name='pokemon_dataset'):
    os.makedirs(dir_name, exist_ok=True)
    base_url = 'https://raw.githubusercontent.com/HybridShivam/Pokemon/master/assets/imagesHQ'

    print(f'\nDescargando {n} pokemones concurrentemente...\n')
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        tasks = [executor.submit(download_one, i, base_url, dir_name) for i in range(1, n + 1)]
        for _ in tqdm(concurrent.futures.as_completed(tasks), total=n, desc="Descargando", unit="img"):
            pass

    total_time = time.time() - start_time
    print(f'  Descarga completada en {total_time:.2f} segundos')
    print(f'  Promedio: {total_time/n:.2f} s/img')
    return total_time


def process_one(image, dir_origin, dir_name):
    try:
        path_origin = os.path.join(dir_origin, image)
        img = Image.open(path_origin).convert('RGB')

        img = img.filter(ImageFilter.GaussianBlur(radius=10))
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        img_inv = ImageOps.invert(img)
        img_inv = img_inv.filter(ImageFilter.GaussianBlur(radius=5))
        width, height = img_inv.size
        img_inv = img_inv.resize((width * 2, height * 2), Image.LANCZOS)
        img_inv = img_inv.resize((width, height), Image.LANCZOS)

        os.makedirs(dir_name, exist_ok=True)
        saving_path = os.path.join(dir_name, image)
        img_inv.save(saving_path, quality=95)
        return True

    except Exception as e:
        return f'Error procesando {image}: {e}'


def process_pokemon_parallel(dir_origin='pokemon_dataset', dir_name='pokemon_processed'):
    os.makedirs(dir_name, exist_ok=True)
    images = sorted([f for f in os.listdir(dir_origin) if f.endswith('.png')])
    total = len(images)

    print(f'\nProcesando {total} imágenes en paralelo...\n')
    start_time = time.time()

    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        tasks = [executor.submit(process_one, img, dir_origin, dir_name) for img in images]
        for _ in tqdm(concurrent.futures.as_completed(tasks), total=total, desc="Procesando", unit="img"):
            pass

    total_time = time.time() - start_time
    print(f'  Procesamiento completado en {total_time:.2f} segundos')
    print(f'  Promedio: {total_time/total:.2f} s/img\n')
    return total_time


if __name__ == '__main__':
    print('='*60)
    print_pikachu()
    print('   POKEMON IMAGE PROCESSING PIPELINE (Optimizado)')
    print('='*60)

    download_time = download_pokemon_concurrent()
    processing_time = process_pokemon_parallel()

    total_time = download_time + processing_time

    print('='*60)
    print('RESUMEN DE TIEMPOS\n')
    print(f'  Descarga:        {download_time:.2f} seg')
    print(f'  Procesamiento:   {processing_time:.2f} seg\n')
    print(f'  Total:           {total_time:.2f} seg')
    print('='*60)