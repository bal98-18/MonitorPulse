# Monitor de Rendimiento de Hardware 

Sistema de monitoreo en tiempo real desarrollado en Python, diseñado para la supervisión de recursos (CPU, RAM, GPU, Disco) con una interfaz gráfica personalizada.

# Características
- **Multi-driver:** Soporte para arquitecturas AMD (vía `LibreHardwareMonitorLib`) y NVIDIA.
- **Interfaz Fluida:** Gráficos circulares dinámicos renderizados con `QPainter`.
- **Arquitectura Escalable:** Implementación de Patrón Factoría para una gestión eficiente de drivers de hardware.
- **Bajo consumo:** Monitoreo optimizado mediante hilos secundarios (`QThread`).

## Requisitos de Instalación
- **Python 3.13+**
- **Windows 10/11**
- Librerías necesarias:
requirements.txt

### NOTA
- El programa se ejecuta siempre como administrador para que pueda leer los archivos .dll (vía `LibreHardwareMonitorLib`)
- Si al ejecutar la aplicación la GPU aparece como "GPU Genérica", por favor verifica que el archivo 'libs/LibreHardwareMonitorLib.dll' no esté bloqueado por Windows (Propiedades -> Desbloquear)

  
