from PySide6 import QtWidgets


class Button(QtWidgets.QPushButton):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setStyleSheet('background-color: #187bcd; color: white')


def create_combobox_layout(label: str, combobox_items: list[str]) -> QtWidgets.QHBoxLayout:
    combobox = QtWidgets.QComboBox()
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
