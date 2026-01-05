import os, sys, logging, csv

from datetime import datetime, timedelta, time
from PyQt6.QtCore import Qt, QCoreApplication, QDate
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QLineEdit, QPushButton, QSpacerItem, QCalendarWidget, QCheckBox, QMessageBox

today = datetime.today().strftime('%Y-%m-%d')
log_path = '\\\\eocservices\\apps$\\programs\\scripts\\logs\\employee_termination_' + today + '.log'
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
        self.open_readme_button.clicked.connect(self.show_readme)
        
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
        tmp_date = self.term_date_calendar.selectedDate().toPyDate()
        today = datetime.today().date()
        now = datetime.now()
        current_time = time(hour=now.hour, minute=now.minute, second=now.second)
        current_date_time = datetime.combine(today, current_time)
        cutoff_time = time(hour=15, minute=0, second=0)
        cutoff_date_time = datetime.combine(today, cutoff_time)
        if (tmp_date < today):
            tmp_date = self.date_by_adding_business_days(today, 0)
            self.disable_immediately(username_text)
        if (tmp_date == today and cutoff_date_time < current_date_time):
            tmp_date = self.date_by_adding_business_days(tmp_date, 1)
            self.disable_immediately(username_text)
        term_date = self.date_by_adding_business_days(tmp_date, 0).strftime('%m/%d/%Y')
        convert_to_shared_date = self.date_by_adding_business_days(tmp_date, 1).strftime("%m/%d/%Y")
        second_notification_date = self.date_by_adding_business_days(tmp_date, 20).strftime('%m/%d/%Y')
        deletion_date = self.date_by_adding_business_days(tmp_date, 30).strftime('%m/%d/%Y')
        final_warning_date = self.date_by_adding_business_days(tmp_date, 29).strftime("%m/%d/%Y")

        current_user = os.environ.get('USER') or os.environ.get('USERNAME')
        logging.info('The following information was submitted by ' + current_user + " to disable " + first_name_text + "'s account")
        
        try:
            self.update_csv(first_name_text,
                            last_name_text,
                            username_text,
                            manager_email_text,
                            hr_email_text,
                            term_date,
                            convert_to_shared_date,
                            second_notification_date,
                            deletion_date,
                            final_warning_date)
        except:
            error_description = 'Failed to update CSV'
            logging.exception(error_description)
            self.show_error_message(error_description)
            QCoreApplication.exit()

        if (immediate_checked):
            try:
                self.disable_immediately(username_text)
            except:
                error_description = 'Failed to create immediate disablement file'
                logging.exception(error_description)
                self.show_error_message(error_description)
                QCoreApplication.exit()

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
                            '\n\nLogs can be reviewed from \\\\eocservices.dartadvantage.com\\apps$\\programs\\scripts\\logs\\'
                            )
        message_box.exec()

    def update_csv(self, first_name, last_name, username, manager, hr, term_date, convert_to_shared_date, second_notification_date, deletion_date, final_warning_date):
        
        logging.info('First name: ' + first_name)
        logging.info('Last name: ' + last_name)
        logging.info('Username: ' + username)
        logging.info('Manager email: ' + manager)
        logging.info('HR email: ' + hr)
        logging.info('Term date: ' + term_date)
        logging.info('Convert to shared mailbox date: ' + convert_to_shared_date)
        logging.info('Second email notification date: ' + second_notification_date)
        logging.info('Final email notification warning date: ' + final_warning_date)
        logging.info('Deletion date: ' + deletion_date)

        term_list_csv = '\\\\eocservices\\apps$\\programs\\scripts\\separation\\term_list.csv'
        logging.info('Begining update of ' + term_list_csv)

        new_data = [(first_name + " " + last_name), first_name, username, manager, hr, term_date, second_notification_date, final_warning_date, deletion_date, convert_to_shared_date]

        with open(term_list_csv, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_data)

    def disable_immediately(self, username):
        immediate_term_path = '\\\\eocservices\\apps$\\programs\\scripts\\separation\\immediate_account_disablement\\' + username

        logging.info('Immediate termination requested, creating file that will trigger immediate account disablement.')

        if not os.path.exists(immediate_term_path):
            with open(immediate_term_path, 'w') as file:
                file.write(username)
            logging.info('Created file ' + immediate_term_path + ', the account will be disabled shortly.')
        else:
            logging.warning('File ' + immediate_term_path + ' already exists. The account should be disabled within a minute. Check the term list for duplicate entries.')

    def show_error_message(self, message):
        error_message_box = QMessageBox()
        error_message_box.setWindowTitle('Error')
        error_message_box.setText(message)
        error_message_box.exec()

    def date_by_adding_business_days(self, from_date, add_days):
        business_days_to_add = add_days
        current_date = from_date
        while business_days_to_add > 0:
            current_date += timedelta(days=1)
            weekday = current_date.weekday()
            if weekday >=5:
                continue
            business_days_to_add -= 1
        return current_date

    def show_readme(self):
        readme_message_box = QMessageBox()
        readme_message_box.setWindowTitle('ReadMe')
        with open('\\\\eocservices\\apps$\\programs\\scripts\\separation\\readme.md') as data:
            readme_message_text = data.read()
        readme_message_box.setText(readme_message_text)
        readme_message_box.exec()
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()