import sys
import serial
import serial.tools.list_ports
import json
import os
from datetime import datetime
from PyQt5 import QtCore, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lectura de sensores")
        self.setGeometry(100, 100, 600, 400)

        # Widgets
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(20, 20, 200, 30)

        self.refreshButton = QtWidgets.QPushButton("Refrescar", self)
        self.refreshButton.setGeometry(240, 20, 100, 30)
        self.refreshButton.clicked.connect(self.refresh_ports)

        self.connectButton = QtWidgets.QPushButton("Conectar", self)
        self.connectButton.setGeometry(360, 20, 100, 30)
        self.connectButton.clicked.connect(self.toggle_connection)

        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(20, 70, 560, 300)

        # Variables
        self.serial = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.read_serial)

        self.timer_guardado = QtCore.QTimer()
        self.timer_guardado.setInterval(60000)  # 60 segundos
        self.timer_guardado.timeout.connect(self.guardar_en_json)

        self.datos_recibidos = []

        self.refresh_ports()

    def refresh_ports(self):
        self.comboBox.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.comboBox.addItem(port.device)

    def toggle_connection(self):
        if self.serial and self.serial.is_open:
            self.timer.stop()
            self.timer_guardado.stop()
            self.serial.close()
            self.connectButton.setText("Conectar")
            self.textEdit.append("Desconectado.")
        else:
            port = self.comboBox.currentText()
            try:
                self.serial = serial.Serial(port, 9600, timeout=1)
                self.connectButton.setText("Desconectar")
                self.textEdit.append(f"Conectado a {port}")

                self.datos_recibidos.clear()
                self.timer.start(100)  # Lectura cada 100 ms
                self.timer_guardado.start()  

            except Exception as e:
                self.textEdit.append(f"Error al conectar: {e}")

    def read_serial(self):
        if self.serial and self.serial.in_waiting:
            try:
                data = self.serial.readline().decode(errors='ignore').strip()
                if data:
                    self.textEdit.append(f"Recibido: {data}")
                    self.datos_recibidos.append(data)
            except Exception as e:
                self.textEdit.append(f"Error leyendo datos: {e}")

    def guardar_en_json(self):
        eventos = []

        for linea in self.datos_recibidos:
            try:
                if "PEATON" in linea.upper():
                    partes = linea.split(":")
                    distancia = int(partes[1]) if len(partes) == 2 and partes[1].isdigit() else None
                    evento = {
                        "fecha": datetime.now().isoformat(),
                        "evento": "PEATON",
                        "distancia_cm": distancia
                    }
                    eventos.append(evento)
            except Exception as e:
                self.textEdit.append(f"Error procesando línea '{linea}': {e}")

        if eventos:
            os.makedirs("datos", exist_ok=True)
            ruta_archivo = os.path.join("datos", "peatones.json")

            # Leer datos anteriores si existen
            try:
                if os.path.exists(ruta_archivo):
                    with open(ruta_archivo, "r") as f:
                        eventos_anteriores = json.load(f)
                else:
                    eventos_anteriores = []
            except Exception:
                eventos_anteriores = []

            eventos_anteriores.extend(eventos)

            try:
                with open(ruta_archivo, "w") as archivo:
                    json.dump(eventos_anteriores, archivo, indent=4)
                self.textEdit.append(f"Datos guardados en {ruta_archivo}")
                self.datos_recibidos.clear()  
            except Exception as e:
                self.textEdit.append(f"Error al guardar JSON: {e}")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
