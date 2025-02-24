from PyQt6.QtWidgets import (QMainWindow, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from compose_window import ComposeWindow
from signup_window import SignupWindow
import pyrebase


class LoginWindow(QMainWindow):
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
        self.setWindowTitle('U-Mail Login')
        self.setFixedSize(925, 500)

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Left side with logo
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        logo_label = QLabel()
        pixmap = QPixmap('login.png')
        logo_label.setPixmap(pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))
        left_layout.addWidget(logo_label)
        layout.addWidget(left_widget)

        # Right side with login form
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # Login form elements
        title_label = QLabel('Sign in')
        title_label.setStyleSheet('color: #57a1f8; font-size: 23px; font-weight: bold;')

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Username')
        self.username_input.setStyleSheet('padding: 10px; border: 1px solid #ccc; border-radius: 5px;')

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet('padding: 10px; border: 1px solid #ccc; border-radius: 5px;')

        login_button = QPushButton('Sign in')
        login_button.setStyleSheet('''
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
        login_button.clicked.connect(self.login)

        signup_layout = QHBoxLayout()
        signup_label = QLabel("Don't have an account?")
        signup_button = QPushButton('Sign up')
        signup_button.setStyleSheet('border: none; color: #57a1f8;')
        signup_button.clicked.connect(self.show_signup)
        signup_layout.addWidget(signup_label)
        signup_layout.addWidget(signup_button)

        self.error_label = QLabel('')
        self.error_label.setStyleSheet('color: red;')

        # Add widgets to right layout
        right_layout.addWidget(title_label)
        right_layout.addWidget(self.username_input)
        right_layout.addWidget(self.password_input)
        right_layout.addWidget(login_button)
        right_layout.addLayout(signup_layout)
        right_layout.addWidget(self.error_label)
        right_layout.addStretch()

        layout.addWidget(right_widget)

    def login(self):
        try:
            firebase = pyrebase.initialize_app(self.firebaseConfig)
            auth = firebase.auth()
            email = self.username_input.text()
            password = self.password_input.text()

            user = auth.sign_in_with_email_and_password(email, password)
            self.compose_window = ComposeWindow(email, user)
            self.compose_window.show()
            self.hide()
        except Exception as e:
            self.error_label.setText('Invalid credentials')

    def show_signup(self):
        self.signup_window = SignupWindow()
        self.signup_window.show()
        self.hide()