import wmi

def probar_lectura_nativa():
    print("Iniciando conexión con sensores de Windows...")
    try:
        w = wmi.WMI()
        controladores = w.Win32_VideoController()
        if controladores:
            print(f"GPU Detectada: {controladores[0].Name.strip()}")
        
        print("\nBuscando uso en los motores (Engines) de la GPU:")
        motores = w.Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine()
        
        encontro_3d = False
        for motor in motores:
            if "3D" in motor.Name:
                encontro_3d = True
                print(f"Proceso [{motor.Name}] -> Uso: {motor.UtilizationPercentage}%")
                
        if not encontro_3d:
            print("No se detectó actividad 3D. (Suele marcar 0% en reposo)")

    except Exception as e:
        print(f"\nError al intentar leer los sensores: {e}")
        print("Asegúrate de ejecutar la consola como Administrador.")

probar_lectura_nativa()