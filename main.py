import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
import MetaTrader5 as mt5


class MT5Interface(QMainWindow):
    def __init__(self):
        super().__init()

        self.setWindowTitle("MT5 Interface")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.connect_button = QPushButton("Conectar a MT5")
        self.connect_button.clicked.connect(self.connect_to_mt5)
        self.layout.addWidget(self.connect_button)

        self.status_label = QLabel()
        self.layout.addWidget(self.status_label)

        self.central_widget.setLayout(self.layout)

    def connect_to_mt5(self):
        # Establecer la dirección del servidor MetaTrader 5
        server = "127.0.0.1:443"  # Reemplaza "port_number" con el número de puerto correcto

        # Usuario y contraseña para tu cuenta de MT5
        account_number = "1003359"
        password = "PaSs5248"

        # Iniciar la conexión con MetaTrader 5
        if mt5.initialize(server):
            # Intentar iniciar sesión en tu cuenta
            login_result = mt5.login(account_number, password)

            if login_result:
                # Obtener la información de la cuenta actual
                account = mt5.account_info()

                # Actualizar la etiqueta de estado
                self.status_label.setText(f"Conectado a MT5. Cuenta: {account['login']}")
            else:
                self.status_label.setText("Error al iniciar sesión. Verifica tus credenciales.")
        else:
            self.status_label.setText("Error al conectarse a MT5. Verifica la dirección del servidor.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MT5Interface()
    window.show()
    sys.exit(app.exec_())

