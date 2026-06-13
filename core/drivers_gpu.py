import os
import sys
import clr 

class BaseGPUDriver:
    #Clase base para asegurar que siempre haya un método get_usage.
    def __init__(self):
        self.nombre = "GPU Genérica"
    def get_usage(self):
        return 0

#DRIVER NVIDIA (Pynvml)
class NvidiaDriver(BaseGPUDriver):
    def __init__(self):
        super().__init__()
        import pynvml
        pynvml.nvmlInit()
        self.handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        self.nombre = "NVIDIA GPU"
    def get_usage(self):
        import pynvml
        return int(pynvml.nvmlDeviceGetUtilizationRates(self.handle).gpu)

#DRIVER AMD (LibreHardwareMonitor + /libs)
class AmdDriver(BaseGPUDriver):
    def __init__(self):
        super().__init__()
        
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dist" )
            
        libs_path = os.path.join(base_path, "libs")
        dll_path = os.path.join(libs_path, "LibreHardwareMonitorLib.dll")
        
        if not os.path.exists(dll_path):
            raise FileNotFoundError(f"DLL no encontrada en: {dll_path}")
            
        sys.path.append(libs_path)
        os.environ["PATH"] += os.pathsep + libs_path
        
        # 3. Carga de ensamblado .NET
        clr.AddReference(dll_path)
        from LibreHardwareMonitor import Hardware
        
        self.computer = Hardware.Computer()
        self.computer.IsGpuEnabled = True
        self.computer.Open()
        
        self.gpu_hw = None
        
        # 1. Primero buscamos explícitamente una GPU AMD (Dedicada o bien detectada)
        for hw in self.computer.Hardware:
            if hw.HardwareType == Hardware.HardwareType.GpuAmd:
                self.gpu_hw = hw
                self.nombre = hw.Name
                break
                
        # 2. Si no encontró una GPU, buscamos una APU (Gráficos integrados en el CPU)
        if not self.gpu_hw:
            for hw in self.computer.Hardware:
                # Nos aseguramos de que sea un CPU y que sea de la marca AMD
                if hw.HardwareType == Hardware.HardwareType.Cpu and "AMD" in hw.Name:
                    self.gpu_hw = hw
                    self.nombre = f"{hw.Name} (Integrated Graphics)"
                    break
        
        if not self.gpu_hw:
            raise Exception("No se detectó GPU AMD")
        
    def get_usage(self):
        from LibreHardwareMonitor import Hardware
        self.gpu_hw.Update()
        for sensor in self.gpu_hw.Sensors:
            if sensor.SensorType == Hardware.SensorType.Load and "Core" in sensor.Name:
                return int(sensor.Value) if sensor.Value is not None else 0
        return 0

class GPUFactory:
    @staticmethod
    def get_driver():
        # Intentar NVIDIA
        try: return NvidiaDriver()
        except: pass
        
        # Intentar AMD
        try: return AmdDriver()
        except Exception as e:
            print(f"[!] Log AMD: {e}")
            
        # Fallback de seguridad
        return BaseGPUDriver()