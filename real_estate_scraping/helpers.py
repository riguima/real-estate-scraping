from PySide6 import QtWidgets
from selenium.webdriver import Firefox
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Button(QtWidgets.QPushButton):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setStyleSheet('background-color: #187bcd; color: white')


def create_combobox_layout(label: str, combobox_items: list[str]) -> QtWidgets.QHBoxLayout:
    combobox = QtWidgets.QComboBox()
    combobox.setObjectName('combobox')
    combobox.addItems(combobox_items)
    layout = QtWidgets.QHBoxLayout()
    layout.addWidget(QtWidgets.QLabel(label), 1)
    layout.addWidget(combobox, 3)
    return layout


def create_layout_directory_dialog(widget: QtWidgets.QWidget) -> QtWidgets.QHBoxLayout:
    input = QtWidgets.QLineEdit()
    button = Button('Selecionar')
    button.clicked.connect(lambda: open_directory_dialog(widget, input))
    layout = QtWidgets.QHBoxLayout()
    layout.addWidget(input)
    layout.addWidget(button)
    return layout


def open_directory_dialog(widget: QtWidgets.QWidget, target_input: QtWidgets.QLineEdit) -> None:
    result = str(QtWidgets.QFileDialog.getExistingDirectory(widget, 'Selecione uma pasta'))
    target_input.setText(result)


def find_element(driver: Firefox, selector: str):
    return WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )


def find_elements(driver: Firefox, selector: str):
    return WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )
