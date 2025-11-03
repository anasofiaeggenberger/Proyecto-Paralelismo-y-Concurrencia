# Proyecto: Paralelismo y Concurrencia — Pokémon Pipeline

## Descripción
Este proyecto descarga y procesa imágenes HD de los primeros 150 Pokémon.  
El objetivo fue optimizar el tiempo de ejecución usando **paralelismo** y **concurrencia**, aprovechando la naturaleza **I/O bound** de la descarga y **CPU bound** del procesamiento.

---

## Nota importante sobre commits
El primer commit del repositorio incluye aproximadamente **2000 cambios**.  
Esto se debió a que inicialmente no se configuró un `.gitignore`, por lo que se subieron archivos del entorno virtual y dependencias locales.  
**Ese commit puede ser ignorado** al revisar el historial, ya que no forma parte del desarrollo real del proyecto.

---

## Estrategia de optimización
- **Descarga concurrente:** implementación con `ThreadPoolExecutor` (tareas I/O bound).  
  → Permite realizar múltiples descargas simultáneas sin bloquear el programa.  
- **Procesamiento paralelo:** implementación con `ProcessPoolExecutor` (tareas CPU bound).  
  → Cada imagen se procesa en un núcleo distinto, aprovechando hasta 8 cores.  
- **Limitación:** se respetó el máximo de **8 núcleos**, según las restricciones del proyecto.  
- Las imágenes continuaron descargándose y procesándose **una a una de forma individual**, tal como se solicitó.

---

## Comparativa de tiempos

| Fase                | Baseline (s) | Optimizado (s) | Mejora (%) |
|---------------------|--------------|----------------|-------------|
| Descarga (I/O)      | 59.04        | 13.21          | **77.63 %** |
| Procesamiento (CPU) | 62.04        | 36.66          | **40.91 %** |
| **Total**           | **121.08**   | **49.86**      | **58.81 %** |

> Los tiempos fueron obtenidos ejecutando ambos scripts en la misma máquina bajo las mismas condiciones.  
> La optimización se logró mediante el uso de `ThreadPoolExecutor` para descargas concurrentes y `ProcessPoolExecutor` para procesamiento paralelo en múltiples núcleos.

---

## Interpretación
La versión optimizada redujo el tiempo total de ejecución de **121.08 s** a **49.86 s**, lo que representa una mejora global de aproximadamente **58.8 %**.  
La mayor ganancia se observó en la fase de **descarga**, donde la concurrencia permitió manejar múltiples solicitudes HTTP simultáneamente.  
El **procesamiento paralelo** también contribuyó significativamente a reducir el tiempo total al distribuir la carga de trabajo entre varios núcleos de CPU.  

En conjunto, los resultados demuestran la eficacia de aplicar **concurrencia** para tareas de entrada/salida y **paralelismo** para tareas computacionalmente intensivas.

---

## Notas adicionales
- Las carpetas `pokemon_dataset/` y `pokemon_processed/` **no están incluidas en el repositorio**, ya que se generan automáticamente al ejecutar el script.  
- `pokemon_dataset/` contiene las imágenes originales descargadas (I/O bound).  
- `pokemon_processed/` contiene las imágenes procesadas con filtros y transformaciones (CPU bound).