from PyQt6.QtWidgets import (QMainWindow, QWidget, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QMessageBox, QTextEdit)
from PyQt6.QtCore import Qt
import imaplib
import email
from email.header import decode_header
import datetime
import pyrebase


class InboxWindow(QMainWindow):
    def __init__(self, user_email, user_data):
        super().__init__()
        self.user_email = user_email
        self.user_data = user_data
        self.imap_server = "imap.gmail.com"
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
        self.load_emails()

    def initUI(self):
        self.setWindowTitle('U-Mail Inbox')
        self.setFixedSize(1000, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Top bar with buttons
        top_bar = QHBoxLayout()
        inbox_button = QPushButton('Inbox')
        inbox_button.setEnabled(False)
        compose_button = QPushButton('Compose')
        compose_button.clicked.connect(self.show_compose)
        refresh_button = QPushButton('Refresh')
        refresh_button.clicked.connect(self.load_emails)

        top_bar.addWidget(inbox_button)
        top_bar.addWidget(compose_button)
        top_bar.addWidget(refresh_button)
        top_bar.addStretch()

        # Email list
        self.email_table = QTableWidget()
        self.email_table.setColumnCount(4)
        self.email_table.setHorizontalHeaderLabels(['From', 'Subject', 'Date', 'Time'])
        self.email_table.horizontalHeader().setStretchLastSection(True)
        self.email_table.clicked.connect(self.show_email_content)

        # Email content viewer
        self.email_content = QTextEdit()
        self.email_content.setReadOnly(True)

        # Add widgets to main layout
        main_layout.addLayout(top_bar)
        main_layout.addWidget(self.email_table)
        main_layout.addWidget(self.email_content)

    def show_compose(self):
        from compose_window import ComposeWindow
        self.compose = ComposeWindow(self.user_email, self.user_data)
        self.compose.show()
        self.hide()

    def load_emails(self):
        try:
            # Load emails from Firebase
            firebase = pyrebase.initialize_app(self.firebaseConfig)
            db = firebase.database()

            # Get all emails where the user is either sender or receiver
            emails = db.child("emails").get()

            self.email_table.setRowCount(0)
            self.emails_data = []

            for email_data in emails.each():
                data = email_data.val()
                if data['receiver'] == self.user_email or data['sender'] == self.user_email:
                    self.emails_data.append(data)
                    row_position = self.email_table.rowCount()
                    self.email_table.insertRow(row_position)

                    # Add email data to table
                    self.email_table.setItem(row_position, 0, QTableWidgetItem(data['sender']))
                    self.email_table.setItem(row_position, 1, QTableWidgetItem(data['subject']))
                    self.email_table.setItem(row_position, 2, QTableWidgetItem(data['date']))
                    self.email_table.setItem(row_position, 3, QTableWidgetItem(data['time']))

            # Also load emails from IMAP
            self.load_imap_emails()

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load emails: {str(e)}')

    def load_imap_emails(self):
        try:
            # Connect to IMAP server
            mail = imaplib.IMAP4_SSL(self.imap_server)
            app_password = os.environ.get('EMAIL_APP_PASSWORD')
            mail.login(self.user_email, app_password)

            # Select inbox
            mail.select('INBOX')

            # Search for all emails
            _, messages = mail.search(None, 'ALL')

            for num in messages[0].split()[-10:]:  # Get last 10 emails
                _, msg = mail.fetch(num, '(RFC822)')
                email_body = msg[0][1]
                email_message = email.message_from_bytes(email_body)

                # Get email details
                subject = decode_header(email_message["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()

                sender = decode_header(email_message["From"])[0][0]
                if isinstance(sender, bytes):
                    sender = sender.decode()

                date = email_message["Date"]

                # Add to table
                row_position = self.email_table.rowCount()
                self.email_table.insertRow(row_position)

                self.email_table.setItem(row_position, 0, QTableWidgetItem(sender))
                self.email_table.setItem(row_position, 1, QTableWidgetItem(subject))
                self.email_table.setItem(row_position, 2, QTableWidgetItem(date))

            mail.logout()

        except Exception as e:
            QMessageBox.warning(self, 'Warning', f'Failed to load IMAP emails: {str(e)}')

    def show_email_content(self):
        try:
            current_row = self.email_table.currentRow()
            if current_row >= 0 and current_row < len(self.emails_data):
                email_data = self.emails_data[current_row]

                content = f"""
                From: {email_data['sender']}
                To: {email_data['receiver']}
                Subject: {email_data['subject']}
                Date: {email_data['date']} {email_data['time']}

                {email_data['msg']}
                """

                self.email_content.setText(content)

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to show email content: {str(e)}')