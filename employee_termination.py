import os, sys, logging

from datetime import datetime
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QLineEdit, QPushButton, QSpacerItem, QCalendarWidget, QCheckBox, QMessageBox

today = datetime.today().strftime('%Y-%m-%d')
log_path = 'C:\\Users\\KVoelker\\repos\\logs\\employee_termination_' + today + '.log'
logging.basicConfig(filename=log_path, level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Assign values for width/height
        text_box_width = 200
        spacer_width = 240
        spacer_height = 15
        calendar_width = 260
        button_width = 260

        self.setWindowTitle("Employee Termination")

        # Create widgets for labels and text input fields
        self.first_name_label = QLabel('First Name:')
        self.first_name_text_box = QLineEdit()
        self.first_name_text_box.setFixedWidth(text_box_width)
        self.first_name_text_box.textChanged.connect(self.check_fields_filled)

        self.last_name_label = QLabel('Last Name:')
        self.last_name_text_box = QLineEdit()
        self.last_name_text_box.setMaximumWidth(text_box_width)
        self.last_name_text_box.textChanged.connect(self.check_fields_filled)

        self.username_label = QLabel('Username:')
        self.username_text_box = QLineEdit()
        self.username_text_box.setFixedWidth(text_box_width)
        self.username_text_box.textChanged.connect(self.check_fields_filled)       

        self.manager_email_label = QLabel('Manager Email:')
        self.manager_email_text_box = QLineEdit()
        self.manager_email_text_box.setFixedWidth(text_box_width)
        self.manager_email_text_box.textChanged.connect(self.check_fields_filled)

        self.hr_email_label = QLabel('HR Email:')
        self.hr_email_text_box = QLineEdit()
        self.hr_email_text_box.setFixedWidth(text_box_width)
        self.hr_email_text_box.textChanged.connect(self.check_fields_filled)

        self.term_date_label = QLabel('Term Date:')
        self.term_date_calendar = QCalendarWidget()
        self.term_date_calendar.setFixedWidth(calendar_width)

        self.immediate_term_label = QLabel('Immediate Termination:')
        self.immediate_term_check_box = QCheckBox()

        self.add_to_term_list_button = QPushButton('Begin Termination Process')
        self.add_to_term_list_button.setFixedWidth(button_width)
        self.add_to_term_list_button.setEnabled(False)
        self.add_to_term_list_button.clicked.connect(self.add_to_term_list)

        self.open_term_list_button = QPushButton('Open Term List')
        self.open_term_list_button.setFixedWidth(button_width)
        
        self.open_readme_button = QPushButton('Open ReadMe')
        self.open_readme_button.setFixedWidth(button_width)
        
        # Create window layout
        layout = QVBoxLayout()
        layout.addWidget(self.first_name_label)
        layout.addWidget(self.first_name_text_box)
        layout.addSpacerItem(QSpacerItem(spacer_width,spacer_height))

        layout.addWidget(self.last_name_label)
        layout.addWidget(self.last_name_text_box)
        layout.addSpacerItem(QSpacerItem(spacer_width,spacer_height))

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_text_box)
        layout.addSpacerItem(QSpacerItem(spacer_width,spacer_height))

        layout.addWidget(self.manager_email_label)
        layout.addWidget(self.manager_email_text_box)
        layout.addSpacerItem(QSpacerItem(spacer_width,spacer_height))

        layout.addWidget(self.hr_email_label)
        layout.addWidget(self.hr_email_text_box)
        layout.addSpacerItem(QSpacerItem(spacer_width,spacer_height))

        layout.addWidget(self.term_date_label)
        layout.addWidget(self.term_date_calendar)
        layout.addSpacerItem(QSpacerItem(spacer_width,spacer_height))

        layout.addWidget(self.immediate_term_label)
        layout.addWidget(self.immediate_term_check_box)
        layout.addSpacerItem(QSpacerItem(spacer_width,spacer_height))
        layout.addSpacerItem(QSpacerItem(spacer_width,spacer_height))

        layout.addWidget(self.add_to_term_list_button)

        layout.addWidget(self.open_term_list_button)

        layout.addWidget(self.open_readme_button)

        # Prevent items from stretching vertically
        layout.insertStretch(-1,1)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
    
    def check_fields_filled(self):
        first_name_text = str(self.first_name_text_box.text())
        last_name_text = str(self.last_name_text_box.text())
        username_text = str(self.username_text_box.text())
        manager_email_text = str(self.manager_email_text_box.text())
        hr_email_text = str(self.hr_email_text_box.text())

        if first_name_text == '' \
            or last_name_text == '' \
            or username_text == '' \
            or manager_email_text == '' \
            or hr_email_text == '':
            self.add_to_term_list_button.setEnabled(False)
        else:
            self.add_to_term_list_button.setEnabled(True)

    def add_to_term_list(self):
        logging.info('########## Begin adding information to termination list ##########')

        first_name_text = str(self.first_name_text_box.text())
        last_name_text = str(self.last_name_text_box.text())
        username_text = str(self.username_text_box.text())
        manager_email_text = str(self.manager_email_text_box.text())
        hr_email_text = str(self.hr_email_text_box.text())
        immediate_checked = self.immediate_term_check_box.isChecked()
        term_date = self.term_date_calendar.selectedDate().toString('MM/dd/yyyy')

        self.update_csv(first_name_text,
                        last_name_text,
                        username_text,
                        manager_email_text,
                        hr_email_text,
                        term_date)

        if (immediate_checked):
            self.disable_immediately(username_text)

        # Popup notifiying what was submitted and where to find logs.
        message_box = QMessageBox()
        message_box.setWindowTitle('Term List Updated')
        message_box.setText('The termination list has been updated with the following information\n' + \
                            '\nFirst name: ' + first_name_text + \
                            '\nLast name: ' + last_name_text + \
                            '\nFull name: ' + first_name_text + ' ' + last_name_text + \
                            '\nUsername: ' + username_text + \
                            '\nManager email: ' + manager_email_text + \
                            '\nHR email: ' + hr_email_text + \
                            '\nImmediate disablement: ' + str(immediate_checked) + \
                            '\nTerm date: ' + term_date + \
                            '\n\nLogs can be reviewed from \\\\eocservices.dartadvantage.com\\apps$\\programs\\path'
                            )
        message_box.exec()

    def update_csv(self, first_name, last_name, username, manager, hr, term_date):
        logging.info('Record of information input by user.')
        logging.info('First name: ' + first_name)
        logging.info('Last name: ' + last_name)
        logging.info('Username: ' + username)
        logging.info('Manager email: ' + manager)
        logging.info('HR email: ' + hr)
        logging.info('Term date: ' + term_date)

        term_list_csv = '\\\\file\\path\\of\\csv\\term_list.csv'
        logging.info('Begining update of ' + term_list_csv)

    def disable_immediately(self, username):
        immediate_term_path = 'C:\\Users\\KVoelker\\repos\\immediate_account_disablement\\' + username

        logging.info('Immediate termination requested, creating file that will trigger immediate account disablement.')

        if not os.path.exists(immediate_term_path):
            with open(immediate_term_path, 'w') as file:
                file.write(username)
            logging.info('Created file ' + immediate_term_path + ', the account will be disabled shortly.')
        else:
            logging.warning('File ' + immediate_term_path + ' already exists. The account should be disabled within a minute. Check the term list for duplicate entries.')
    
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()