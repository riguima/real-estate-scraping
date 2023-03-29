from PySide6 import QtWidgets
import sys

from helpers import (
    create_combobox_layout, create_layout_directory_dialog,
    Button,
)


class Main(QtWidgets.QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet('font-size: 20px')
        self.setFixedSize(400, 250)
        self.layout_website = create_combobox_layout('Site', ['Zap Imóveis'])
        self.layout_city = create_combobox_layout('Cidade', ['Itupeva - SP'])
        self.layout_type = create_combobox_layout('Tipo', ['Casa', 'Apartamento'])
        self.layout_directory_dialog = create_layout_directory_dialog(self)
        self.button = Button('Gerar Planilha')
        self.button.clicked.connect(self.generate_spreadsheet)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.layout_website)
        self.layout.addLayout(self.layout_city)
        self.layout.addLayout(self.layout_type)
        self.layout.addLayout(self.layout_directory_dialog)
        self.layout.addWidget(self.button)

    def generate_spreadsheet(self) -> None:
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = Main()
    widget.show()
    sys.exit(app.exec())
