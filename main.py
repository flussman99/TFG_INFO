import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
import MetaTrader4 as mt4
import MetaTrader4.constants as mt4c

class MT4Interface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MT4 Interface")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.connect_button = QPushButton("Conectar a MT4")
        self.connect_button.clicked.connect(self.connect_to_mt4)
        self.layout.addWidget(self.connect_button)

        self.status_label = QLabel()
        self.layout.addWidget(self.status_label)

        self.central_widget.setLayout(self.layout)

    def connect_to_mt4(self):
        # Establecer la dirección del servidor MetaTrader 4
        server = "127.0.0.1:port_number"  # Reemplace "port_number" con el número de puerto correcto

        # Iniciar la conexión con MetaTrader 4
        mt4.initialize(server)

        # Obtener la cuenta actual
        account = mt4.account_info()

        # Actualizar la etiqueta de estado
        self.status_label.setText(f"Conectado a MT4. Cuenta: {account}")

        # Finalizar la conexión con MetaTrader 4 (debe agregar un botón para cerrar la conexión)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MT4Interface()
    window.show()
    sys.exit(app.exec_())
