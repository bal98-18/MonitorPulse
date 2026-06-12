import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setStyleSheet(open("assets/styles.qss").read())
    ventana = MainWindow()
    ventana.show()
    
    sys.exit(app.exec())