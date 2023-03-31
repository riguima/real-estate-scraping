from PySide6 import QtWidgets
import sys
from pathlib import Path

from real_estate_scraping.helpers import (
    create_combobox_layout, create_layout_directory_dialog,
    Button
)
from real_estate_scraping.use_cases import get_cities, to_excel
from real_estate_scraping.adapters import ZapImoveisBrowser


class Main(QtWidgets.QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet('font-size: 20px')
        self.setFixedSize(400, 250)
        self.layout_website = create_combobox_layout(self, 'Site', ['Zap Imóveis'])
        self.layout_city = create_combobox_layout(self, 'Cidade', get_cities())
        self.layout_type = create_combobox_layout(self, 'Tipo', ['Casa', 'Apartamento'])
        self.layout_negotiation_type = create_combobox_layout(self, 'Tipo de negociação', ['Venda', 'Aluguel'])
        self.layout_directory_dialog = create_layout_directory_dialog(self)
        self.button = Button('Gerar Planilha')
        self.button.clicked.connect(self.to_excel)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.layout_website)
        self.layout.addLayout(self.layout_city)
        self.layout.addLayout(self.layout_negotiation_type)
        self.layout.addLayout(self.layout_type)
        self.layout.addLayout(self.layout_directory_dialog)
        self.layout.addWidget(self.button)

    def to_excel(self) -> None:
        browser = ZapImoveisBrowser()
        city, real_estate_type, negotiation_type = self.findChildren(QtWidgets.QComboBox)[1:]
        browser.search(city.currentText(), real_estate_type.currentText(), negotiation_type.currentText())
        to_excel(browser.create_real_estates(), 'result.xlsx')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = Main()
    widget.show()
    sys.exit(app.exec())
