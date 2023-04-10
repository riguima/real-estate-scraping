from PySide6 import QtWidgets
from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Button(QtWidgets.QPushButton):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setStyleSheet('background-color: #187bcd; color: white')


def create_combobox_layout(parent: QtWidgets.QWidget, label: str,
                           combobox_items: list[str]) -> QtWidgets.QHBoxLayout:
    combobox = QtWidgets.QComboBox(parent)
    combobox.addItems(combobox_items)
    layout = QtWidgets.QHBoxLayout()
    layout.addWidget(QtWidgets.QLabel(label), 1)
    layout.addWidget(combobox, 3)
    return layout


def create_layout_directory_dialog(widget: QtWidgets.QWidget
                                   ) -> QtWidgets.QHBoxLayout:
    line_edit = QtWidgets.QLineEdit(widget)
    button = Button('Selecionar')
    button.clicked.connect(lambda: open_directory_dialog(widget, line_edit))
    layout = QtWidgets.QHBoxLayout()
    layout.addWidget(line_edit)
    layout.addWidget(button)
    return layout


def open_directory_dialog(widget: QtWidgets.QWidget,
                          target_input: QtWidgets.QLineEdit) -> None:
    result = str(QtWidgets.QFileDialog.getExistingDirectory(
        widget, 'Selecione uma pasta'))
    target_input.setText(result)


def find_element(driver: Chrome, selector: str):
    return WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )


def find_elements(driver: Chrome, selector: str):
    return WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )


def click(driver: Chrome, selector: str) -> None:
    driver.execute_script('arguments[0].click();', find_element(selector))
