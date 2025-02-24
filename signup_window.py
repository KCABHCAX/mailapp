from PyQt6.QtWidgets import (QMainWindow, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt
import re
import pyrebase


class SignupWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.firebaseConfig = {
            'apiKey': "AIzaSyDYq0qeh4RybLnazTrzCZ7_YQQvox8qpGY",
            'authDomain': "unitym-6607e.firebaseapp.com",
            'databaseURL': "https://unitym-6607e.firebaseio.com",
            'projectId': "unitym-6607e",
            'storageBucket': "unitym-6607e.appspot.com",
            'messagingSenderId': "136686396771",
            'appId': "1:136686396771:web:de5dee385a09b3a7bf1f56",
            'measurementId': "G-0VG8WD1D3T"
        }
        self.initUI()

    def initUI(self):
        self.setWindowTitle('U-Mail Sign Up')
        self.setFixedSize(600, 500)

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Signup form elements
        title_label = QLabel('Create Account')
        title_label.setStyleSheet('color: #57a1f8; font-size: 23px; font-weight: bold;')

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Name')
        self.name_input.setStyleSheet('padding: 10px; border: 1px solid #ccc; border-radius: 5px;')

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Username @unity.com')
        self.email_input.setStyleSheet('padding: 10px; border: 1px solid #ccc; border-radius: 5px;')

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet('padding: 10px; border: 1px solid #ccc; border-radius: 5px;')

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText('Confirm Password')
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setStyleSheet('padding: 10px; border: 1px solid #ccc; border-radius: 5px;')

        signup_button = QPushButton('Sign up')
        signup_button.setStyleSheet('''
            QPushButton {
                background-color: #57a1f8;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4a8fe6;
            }
        ''')
        signup_button.clicked.connect(self.signup)

        self.error_label = QLabel('')
        self.error_label.setStyleSheet('color: red;')

        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(signup_button)
        layout.addWidget(self.error_label)
        layout.addStretch()

    def check_password_strength(self, password):
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True

    def signup(self):
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not name:
            self.error_label.setText('Please Enter Name')
            return

        if '@unity.com' not in email:
            self.error_label.setText('Please use @unity.com')
            return

        if password != confirm_password:
            self.error_label.setText('Passwords do not match')
            return

        if not self.check_password_strength(password):
            self.error_label.setText('Please use a strong password')
            return

        try:
            firebase = pyrebase.initialize_app(self.firebaseConfig)
            auth = firebase.auth()
            user = auth.create_user_with_email_and_password(email, password)

            QMessageBox.information(self, 'Success', 'Account created successfully!')
            self.close()

        except Exception as e:
            self.error_label.setText('Account already exists')