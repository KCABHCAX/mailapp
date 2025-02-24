from PyQt6.QtWidgets import (QMainWindow, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QTextEdit, QMenuBar,
                             QMenu, QMessageBox, QHBoxLayout)
from PyQt6.QtCore import Qt
import datetime
import pyrebase
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


class ComposeWindow(QMainWindow):
    def __init__(self, user_email, user_data):
        super().__init__()
        self.user_email = user_email
        self.user_data = user_data
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.firebaseConfig = {
            'apiKey': "AIzaSyDYq0qeh4RybLnazTrzCZ7_YQQvox8qpGY",
            'authDomain': "unitym-6607e.firebaseapp.com",
            'databaseURL': "https://unitym-6607e-default-rtdb.firebaseio.com/",
            'projectId': "unitym-6607e",
            'storageBucket': "unitym-6607e.appspot.com",
            'messagingSenderId': "136686396771",
            'appId': "1:136686396771:web:de5dee385a09b3a7bf1f56",
            'measurementId': "G-0VG8WD1D3T"
        }
        self.initUI()

    def initUI(self):
        self.setWindowTitle('U-Mail Compose')
        self.setFixedSize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Top bar with buttons
        top_bar = QHBoxLayout()
        inbox_button = QPushButton('Inbox')
        inbox_button.clicked.connect(self.show_inbox)
        compose_button = QPushButton('Compose')
        compose_button.setEnabled(False)

        top_bar.addWidget(inbox_button)
        top_bar.addWidget(compose_button)
        top_bar.addStretch()

        # Email composition form
        form_layout = QVBoxLayout()

        title_label = QLabel('Compose Email')
        title_label.setStyleSheet('color: #57a1f8; font-size: 23px; font-weight: bold;')

        self.to_input = QLineEdit()
        self.to_input.setPlaceholderText('To:')
        self.to_input.setStyleSheet('padding: 10px; border: 1px solid #ccc; border-radius: 5px;')

        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText('Subject:')
        self.subject_input.setStyleSheet('padding: 10px; border: 1px solid #ccc; border-radius: 5px;')

        self.message_input = QTextEdit()
        self.message_input.setStyleSheet('padding: 10px; border: 1px solid #ccc; border-radius: 5px;')

        # Buttons layout
        buttons_layout = QHBoxLayout()

        send_button = QPushButton('Send')
        send_button.setStyleSheet('''
            QPushButton {
                background-color: #57a1f8;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #4a8fe6;
            }
        ''')
        send_button.clicked.connect(self.send_email)

        draft_button = QPushButton('Save Draft')
        draft_button.setStyleSheet('''
            QPushButton {
                background-color: #gray;
                color: black;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                min-width: 100px;
            }
        ''')
        draft_button.clicked.connect(self.save_draft)

        buttons_layout.addWidget(send_button)
        buttons_layout.addWidget(draft_button)
        buttons_layout.addStretch()

        # Add all layouts to main layout
        main_layout.addLayout(top_bar)
        main_layout.addWidget(title_label)
        main_layout.addWidget(self.to_input)
        main_layout.addWidget(self.subject_input)
        main_layout.addWidget(self.message_input)
        main_layout.addLayout(buttons_layout)

    def show_inbox(self):
        from inbox_window import InboxWindow
        self.inbox = InboxWindow(self.user_email, self.user_data)
        self.inbox.show()
        self.hide()

    def send_email(self):
        try:
            # Get email details
            to_email = self.to_input.text()
            subject = self.subject_input.text()
            message = self.message_input.toPlainText()

            # Create MIME message
            msg = MIMEMultipart()
            msg['From'] = self.user_email
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            # Connect to SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()

            # Login with app-specific password
            app_password = os.environ.get('EMAIL_APP_PASSWORD')  # Set this in your environment variables
            server.login(self.user_email, app_password)

            # Send email
            server.send_message(msg)
            server.quit()

            # Save to Firebase
            firebase = pyrebase.initialize_app(self.firebaseConfig)
            db = firebase.database()

            now = datetime.datetime.now()
            data = {
                "sender": self.user_email,
                "receiver": to_email,
                "subject": subject,
                "msg": message,
                "date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%H:%M:%S"),
                "status": "sent"
            }

            db.child("emails").push(data)

            QMessageBox.information(self, 'Success', 'Email sent successfully!')
            self.clear_form()

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to send email: {str(e)}')

    def save_draft(self):
        try:
            firebase = pyrebase.initialize_app(self.firebaseConfig)
            db = firebase.database()

            now = datetime.datetime.now()
            data = {
                "sender": self.user_email,
                "receiver": self.to_input.text(),
                "subject": self.subject_input.text(),
                "msg": self.message_input.toPlainText(),
                "date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%H:%M:%S"),
                "status": "draft"
            }

            db.child("emails").push(data)
            QMessageBox.information(self, 'Success', 'Draft saved successfully!')

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save draft: {str(e)}')

    def clear_form(self):
        self.to_input.clear()
        self.subject_input.clear()
        self.message_input.clear()