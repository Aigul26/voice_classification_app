import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QFileDialog, QMessageBox
)

API_BASE_URL = "http://127.0.0.1:8001" # FIXME: достать из .env

class VoiceClassificationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.token = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Voice Classification App")
        self.setFixedSize(400, 300)
        layout = QVBoxLayout()

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Login")
        layout.addWidget(self.login_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        layout.addWidget(self.name_input)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)



        self.upload_button = QPushButton("Upload MP3 for Classification")
        self.upload_button.setEnabled(False)
        self.upload_button.clicked.connect(self.upload_audio)
        layout.addWidget(self.upload_button)

        self.result_label = QLabel("Result will appear here")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def register(self):
        login = self.login_input.text()
        password = self.password_input.text()
        name = self.name_input.text()

        if not login or not password or not name:
            self.show_error("Login, password, and name are required.")
            return

        data = {
            "login": login,
            "password": password,
            "name": name
        }

        try:
            response = requests.post(f"{API_BASE_URL}/register", json=data)
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "User registered.")
            else:
                self.show_error(response)
        except Exception as e:
            self.show_error(str(e))

    def login(self):
        login = self.login_input.text()
        password = self.password_input.text()

        if not login or not password:
            self.show_error("Login and password required.")
            return

        data = {"username": login, "password": password}
        try:
            response = requests.post(f"{API_BASE_URL}/token", data=data)
            if response.status_code == 200:
                self.token = response.json()["access_token"]
                self.upload_button.setEnabled(True)
                QMessageBox.information(self, "Success", "Logged in successfully.")
            else:
                self.show_error(response)
        except Exception as e:
            self.show_error(str(e))

    def upload_audio(self):

        if not self.token: 
            self.show_error("You must be logged in.")
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select MP3 File", "", "MP3 Files (*.mp3)"
        )

        if not file_path:
            return

        try:
            with open(file_path, "rb") as file:
                files = {"mp3_file": file}
                headers = {"Authorization": f"Bearer {self.token}"}
                response = requests.post(
                    f"{API_BASE_URL}/classification_file", files=files, headers=headers
                )

            if response.status_code == 200:
                result = response.json()
                print(f"Result: {result}")
                self.result_label.setText(f"Predicted class: {result['predicted_class']}")
            else:
                self.show_error(response)
        except Exception as e:
            self.show_error(str(e))

    def show_error(self, error):
        if isinstance(error, requests.Response):
            try:
                msg = error.json().get("detail", error.text)
            except Exception:
                msg = error.text
            QMessageBox.warning(self, "Error", f"{msg}")
        else:
            QMessageBox.warning(self, "Error", str(error))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoiceClassificationApp()
    window.show()
    sys.exit(app.exec_())
