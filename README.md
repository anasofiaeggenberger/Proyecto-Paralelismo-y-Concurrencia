# Proyecto: Paralelismo y Concurrencia — Pokémon Pipeline

## Descripción
Este proyecto descarga y procesa imágenes HD de los primeros 150 Pokémon.
El objetivo fue optimizar el tiempo de ejecución usando paralelismo y concurrencia, aprovechando la naturaleza **I/O bound** de la descarga y **CPU bound** del procesamiento.

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
| Descarga (I/O)      | 59.04        | 13.21          | **77.6 %** |
| Procesamiento (CPU) | 62.04        | 36.66          | **40.9 %** |
| **Total**           | **121.08**   | **49.86**      | **58.8 %** |

> Los tiempos fueron medidos en la misma máquina, ejecutando las 150 imágenes en ambas versiones.  
> La mejora se obtuvo mediante el uso de `ThreadPoolExecutor` para descargas concurrentes y `ProcessPoolExecutor` para procesamiento paralelo.

---

## Interpretación
La versión optimizada redujo el tiempo total de ejecución de **121.08 s a 49.86 s**, lo que representa una mejora global del **58.8 %**.  
La mayor ganancia se logró en la fase de descarga gracias a la concurrencia (I/O bound), aunque el procesamiento paralelo también aportó una mejora significativa.  
Esto demuestra la efectividad de combinar **concurrencia para operaciones de entrada/salida** y **paralelismo para tareas intensivas en CPU**.

---