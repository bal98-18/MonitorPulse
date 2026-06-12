from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
import time
from core.medidor import MedidorHardware

#Optimazación de la Aplicación
class LectorThread(QThread):
    datos_actualizados = pyqtSignal(dict)

    def run(self):
        medidor = MedidorHardware()
        while True:
            datos = medidor.obtener_datos()
            self.datos_actualizados.emit(datos)
            time.sleep(1) 

class GraficaCircular(QWidget):
    def __init__(self, titulo, color_hex):
        super().__init__()
        self.valor = 0
        self.titulo = titulo
        self.color_borde = QColor(color_hex)
        self.color_fondo = QColor("#2D2D30")
        self.setFixedSize(140, 140)

    def actualizar_valor(self, nuevo_valor):
        self.valor = nuevo_valor
        self.update() 

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(10, 10, self.width() - 20, self.height() - 20)
        
        pen_fondo = QPen(self.color_fondo, 12)
        pen_fondo.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen_fondo)
        painter.drawArc(rect, 0, 360 * 16)

        pen_progreso = QPen(self.color_borde, 12)
        pen_progreso.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen_progreso)
        angulo_inicio = 270 * 16 
        angulo_span = int(-(self.valor / 100.0) * 360 * 16)
        painter.drawArc(rect, angulo_inicio, angulo_span)

        painter.setPen(Qt.GlobalColor.white)
        painter.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{int(self.valor)}%")

        painter.setFont(QFont("Segoe UI", 9))
        rect_titulo = QRectF(10, 30, self.width() - 20, self.height() - 20)
        painter.drawText(rect_titulo, Qt.AlignmentFlag.AlignCenter, self.titulo)
        painter.end()

# Tarjeta que agrupa el círculo y el texto inferior
class TagComponente(QWidget):
    def __init__(self, titulo, color_hex):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.grafica = GraficaCircular(titulo, color_hex)
        
        self.label_info = QLabel("Cargando info...")
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_info.setStyleSheet("color: #B0B0B0; font-family: 'Segoe UI'; font-size: 11px;")
        self.label_info.setWordWrap(True) 
        
        layout.addWidget(self.grafica, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_info, alignment=Qt.AlignmentFlag.AlignTop)
        
        self.setLayout(layout)
        self.setFixedSize(160, 210) 

    def actualizar(self, datos_componente):
        self.grafica.actualizar_valor(datos_componente["uso"])
        self.label_info.setText(datos_componente["info"])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MonitorPulse")
        self.setFixedSize(720, 260)
        self.setStyleSheet("background-color: #1E1E1E;")

        widget_central = QWidget()
        layout_principal = QHBoxLayout()
        widget_central.setLayout(layout_principal)
        self.setCentralWidget(widget_central)

        self.tarjeta_cpu = TagComponente("CPU", "#00E676")   
        self.tarjeta_ram = TagComponente("RAM", "#2979FF")   
        self.tarjeta_gpu = TagComponente("GPU", "#FF3D00")   
        self.tarjeta_disco = TagComponente("DISCO", "#FFC107") 

        layout_principal.addWidget(self.tarjeta_cpu)
        layout_principal.addWidget(self.tarjeta_ram)
        layout_principal.addWidget(self.tarjeta_gpu)
        layout_principal.addWidget(self.tarjeta_disco)

        self.hilo = LectorThread()
        self.hilo.datos_actualizados.connect(self.actualizar_interfaz)
        self.hilo.start()

    def actualizar_interfaz(self, datos):
        self.tarjeta_cpu.actualizar(datos["cpu"])
        self.tarjeta_ram.actualizar(datos["ram"])
        self.tarjeta_gpu.actualizar(datos["gpu"])
        self.tarjeta_disco.actualizar(datos["disco"])