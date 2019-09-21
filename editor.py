import traceback

from PyQt5.QtWidgets import QLineEdit, QAbstractItemView, QFileDialog, QCheckBox, QWidget, QLabel, QTextEdit, \
    QTabWidget, QComboBox, QGridLayout

from core import *
from Utility.ui_utility import *


class HistoryEditor(QWidget):
    def __init__(self, parent: QWidget):
        super(HistoryEditor, self).__init__(parent)

        self.__events = []
        self.__source = ''
        self.__current_event = None

        self.__tab_main = QTabWidget()
        # self.__combo_depot = QComboBox()
        self.__combo_events = QComboBox()

        self.__label_uuid = QLabel()
        self.__line_time = QLineEdit()
        self.__line_location = QLineEdit()
        self.__line_people = QLineEdit()
        self.__line_organization = QLineEdit()
        self.__line_default_tags = QLineEdit()

        self.__button_auto_time = QPushButton('Auto Detect')
        self.__button_auto_location = QPushButton('Auto Detect')
        self.__button_auto_people = QPushButton('Auto Detect')
        self.__button_auto_organization = QPushButton('Auto Detect')

        self.__line_title = QLineEdit()
        self.__text_brief = QTextEdit()
        self.__text_event = QTextEdit()

        self.__table_tags = EasyQTableWidget()

        self.__button_new = QPushButton('New')
        self.__button_apply = QPushButton('Apply')
        self.__button_cancel = QPushButton('Cancel')

        self.init_ui()
        self.config_ui()

    def init_ui(self):
        root_layout = QVBoxLayout()

        line = QHBoxLayout()
        line.addWidget(self.__combo_events, 1)
        line.addWidget(self.__button_new, 0)

        root_layout.addLayout(line)
        root_layout.addWidget(self.__tab_main)
        root_layout.addLayout(horizon_layout([self.__button_apply, self.__button_cancel]))
        self.setLayout(root_layout)

        event_page_layout = create_new_tab(self.__tab_main, 'Event Editor')

        property_layout = QGridLayout()

        property_layout.addWidget(QLabel('Event ID'), 0, 0)
        property_layout.addWidget(self.__label_uuid, 0, 1)

        property_layout.addWidget(QLabel('Event Time'), 1, 0)
        property_layout.addWidget(self.__line_time, 1, 1)
        property_layout.addWidget(self.__button_auto_time, 1, 2)

        property_layout.addWidget(QLabel('Event Location'), 2, 0)
        property_layout.addWidget(self.__line_location, 2, 1)
        property_layout.addWidget(self.__button_auto_location, 2, 2)

        property_layout.addWidget(QLabel('Event Participant'), 3, 0)
        property_layout.addWidget(self.__line_people, 3, 1)
        property_layout.addWidget(self.__button_auto_people, 3, 2)

        property_layout.addWidget(QLabel('Event Organization'), 4, 0)
        property_layout.addWidget(self.__line_organization, 4, 1)
        property_layout.addWidget(self.__button_auto_organization, 4, 2)

        property_layout.addWidget(QLabel('Event Tags'), 5, 0)
        property_layout.addWidget(self.__line_default_tags, 5, 1)

        event_page_layout.addLayout(property_layout)

        event_page_layout.addWidget(QLabel('Event Title'))
        event_page_layout.addWidget(self.__line_title)

        event_page_layout.addWidget(QLabel('Event Brief'))
        event_page_layout.addWidget(self.__text_brief, 2)

        event_page_layout.addWidget(QLabel('Event Description'))
        event_page_layout.addWidget(self.__text_event, 5)

        ltags_page_layout = create_new_tab(self.__tab_main, 'Label Tag Editor')
        ltags_page_layout.addWidget(self.__table_tags)

        self.setMinimumSize(700, 500)

    def config_ui(self):
        self.__button_auto_time.clicked.connect(self.on_button_auto_time)
        self.__button_auto_location.clicked.connect(self.on_button_auto_location)
        self.__button_auto_people.clicked.connect(self.on_button_auto_people)
        self.__button_auto_organization.clicked.connect(self.on_button_auto_organization)

        self.__button_new.clicked.connect(self.on_button_new)
        self.__button_apply.clicked.connect(self.on_button_apply)
        self.__button_cancel.clicked.connect(self.on_button_cancel)

    # ---------------------------------------------------- Features ----------------------------------------------------

    def load_event(self, event: History.Event):
        self.__label_uuid.setText(LabelTagParser.tags_to_text(event.uuid()))
        self.__line_time.setText(LabelTagParser.tags_to_text(event.time()))

        self.__line_location.setText(LabelTagParser.tags_to_text(event.tags('location')))
        self.__line_people.setText(LabelTagParser.tags_to_text(event.tags('people')))
        self.__line_organization.setText(LabelTagParser.tags_to_text(event.tags('location')))
        self.__line_default_tags.setText(LabelTagParser.tags_to_text(event.tags('tags')))

        self.__line_title.setText(LabelTagParser.tags_to_text(event.title()))
        self.__text_brief.setText(LabelTagParser.tags_to_text(event.brief()))
        self.__text_event.setText(LabelTagParser.tags_to_text(event.event()))

    def set_events(self, events: History.Event or [History.Event], source: str):
        self.__events = events if isinstance(events, list) else [events]
        self.__source = source

        self.__combo_events.clear()
        for event in self.__events:
            self.__combo_events.addItem(event.uuid())

    # ---------------------------------------------------- UI Event ----------------------------------------------------

    def on_button_auto_time(self):
        pass

    def on_button_auto_location(self):
        pass

    def on_button_auto_people(self):
        pass

    def on_button_auto_organization(self):
        pass

    def on_button_new(self):
        if self.__current_event is not None:
            pass
        self.__current_event = History.Event()
        self.load_event(self.__current_event)
        self.__combo_events.setEditText(self.__current_event.uuid())

    def on_button_apply(self):
        if self.__current_event is None:
            self.__current_event = History.Event()
        else:
            self.__current_event.reset()

        input_time = self.__line_time.text()
        input_location = self.__line_location.text()
        input_people = self.__line_people.text()
        input_organization = self.__line_organization.text()
        input_default_tags = self.__line_default_tags.text()

        input_title = self.__line_title.text()
        input_brief = self.__text_brief.toPlainText()
        sinput_event = self.__text_event.toPlainText()

        self.__current_event.set_label_tags('time',         input_time.split(','))
        self.__current_event.set_label_tags('location',     input_location.split(','))
        self.__current_event.set_label_tags('people',       input_people.split(','))
        self.__current_event.set_label_tags('organization', input_organization.split(','))
        self.__current_event.set_label_tags('tags',         input_default_tags.split(','))

        self.__current_event.set_label_tags('title', input_title)
        self.__current_event.set_label_tags('brief', input_brief)
        self.__current_event.set_label_tags('event', sinput_event)

        result = False
        if len(self.__events) == 0:
            source = str(self.__current_event.uuid()) + '.his'
            result = History.Loader().to_local_depot(
                self.__current_event, 'China', source)
        else:
            # The whole file should be updated
            if self.__current_event not in self.__events:
                self.__events.append(self.__current_event)
            source = self.__events[0].source()
            if source is None or len(source) == 0:
                source = str(self.__current_event.uuid()) + '.his'
                result = History.Loader().to_local_depot(self.__events, 'China', source)

        tips = 'Save Successful.' if result else 'Save Fail.'
        if len(source) > 0:
            tips += '\nSave File: ' + source
        QMessageBox.information(self, 'Save', tips, QMessageBox.Ok)

    def on_button_cancel(self):
        if self.parent() is not None:
            self.parent().close()
        else:
            self.close()


def main():
    app = QApplication(sys.argv)

    dlg = QDialog()
    layout = QVBoxLayout()
    layout.addWidget(HistoryEditor(dlg))
    dlg.setLayout(layout)
    dlg.exec()


# ----------------------------------------------------------------------------------------------------------------------

def exception_hook(type, value, tback):
    # log the exception here
    print('Exception hook triggered.')
    print(type)
    print(value)
    print(tback)
    # then call the default handler
    sys.__excepthook__(type, value, tback)


if __name__ == "__main__":
    sys.excepthook = exception_hook
    try:
        main()
    except Exception as e:
        print('Error =>', e)
        print('Error =>', traceback.format_exc())
        exit()
    finally:
        pass



