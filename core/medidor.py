import psutil
import wmi
from core.drivers_gpu import GPUFactory

class MedidorHardware:
    def __init__(self):
        self.gpu_driver = GPUFactory.get_driver()
        
        try:
            self.w = wmi.WMI()
            self.cpu_nombre = self.w.Win32_Processor()[0].Name.strip()
        except Exception:
            self.w = None
            self.cpu_nombre = "CPU Desconocida"

        self.ram_total_gb = psutil.virtual_memory().total / (1024**3)
        self.disco_total_gb = psutil.disk_usage('C:\\').total / (1024**3)

    def obtener_datos(self):
        ram = psutil.virtual_memory()
        disco = psutil.disk_usage('C:\\')
        
        return {
            "cpu": {
                "uso": psutil.cpu_percent(interval=None),
                "info": self.cpu_nombre
            },
            "ram": {
                "uso": ram.percent,
                "info": f"{ram.available / (1024**3):.1f} GB libres de {self.ram_total_gb:.1f} GB"
            },
            "gpu": {
                "uso": self.gpu_driver.get_usage(), 
                "info": self.gpu_driver.nombre
            },
            "disco": {
                "uso": disco.percent,
                "info": f"{disco.free / (1024**3):.1f} GB libres de {self.disco_total_gb:.1f} GB"
            }
        }