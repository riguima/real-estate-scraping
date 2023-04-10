from PySide6 import QtWidgets, QtGui
import sys
from pathlib import Path
import pandas as pd

from real_estate_scraping.helpers import (
    create_combobox_layout, create_layout_directory_dialog,
    Button
)
from real_estate_scraping.domain import SearchInfo
from real_estate_scraping.use_cases import (
    get_cities, append_to_df
)
from real_estate_scraping.adapters import ZapImoveisBrowser, ImovelWebBrowser


class Main(QtWidgets.QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.message_box = QtWidgets.QMessageBox()
        self.setStyleSheet('font-size: 20px')
        self.setFixedSize(400, 300)
        self.layout_website = create_combobox_layout(
            self, 'Site', ['Zap Imóveis', 'Imóvel Web'])
        self.layout_city = create_combobox_layout(self, 'Cidade', get_cities())
        self.layout_type = create_combobox_layout(
            self, 'Tipo', ['Casas', 'Apartamentos'])
        self.layout_negotiation_type = create_combobox_layout(
            self, 'Tipo de negociação', ['Venda', 'Aluguel'])
        self.label_neighborhood = QtWidgets.QLabel('Bairro')
        self.input_neighborhood = QtWidgets.QLineEdit()
        self.layout_neighborhood = QtWidgets.QHBoxLayout()
        self.layout_neighborhood.addWidget(self.label_neighborhood)
        self.layout_neighborhood.addWidget(self.input_neighborhood)
        self.label_num_pages = QtWidgets.QLabel('Número de páginas')
        self.input_num_pages = QtWidgets.QLineEdit()
        self.input_num_pages.setValidator(QtGui.QIntValidator())
        self.layout_num_pages = QtWidgets.QHBoxLayout()
        self.layout_num_pages.addWidget(self.label_num_pages)
        self.layout_num_pages.addWidget(self.input_num_pages)
        self.layout_directory_dialog = create_layout_directory_dialog(self)
        self.button = Button('Gerar Planilha')
        self.button.clicked.connect(self.to_excel)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.layout_website)
        self.layout.addLayout(self.layout_city)
        self.layout.addLayout(self.layout_negotiation_type)
        self.layout.addLayout(self.layout_type)
        self.layout.addLayout(self.layout_neighborhood)
        self.layout.addLayout(self.layout_num_pages)
        self.layout.addLayout(self.layout_directory_dialog)
        self.layout.addWidget(self.button)

    def to_excel(self) -> None:
        self.message_box.show()
        self.message_box.setText('Coletando os dados...')
        if self.findChildren(
            QtWidgets.QComboBox
        )[0].currentText() == 'Imóvel Web':
            browser = ImovelWebBrowser()
        else:
            browser = ZapImoveisBrowser()
        path = str(Path(self.findChild(
            QtWidgets.QLineEdit
        ).text()) / 'result.xlsx')
        if Path(path).exists():
            df = pd.read_excel(path)
        else:
            df = pd.DataFrame(columns=[
                'Tipo de negociação', 'Tipo do imóvel', 'Cidade',
                'Contato do anunciante', 'Nome do anunciante', 'Preço',
                'Endereço', 'Área', 'Área útil', 'Quartos', 'Banheiros',
                'Vagas', 'Data da publicação', 'Link',
            ])
        city, real_estate_type, negotiation_type = self.findChildren(
            QtWidgets.QComboBox)[1:]
        city, state = city.currentText().split(' - ')
        search_info = SearchInfo(
            city, state, self.input_neighborhood.text(),
            negotiation_type.currentText(), real_estate_type.currentText(),
            int(self.input_num_pages.text()),
        )
        real_estates = browser.create_real_estates(search_info, df)
        df = append_to_df(real_estates, df)
        df.to_excel(path, index=False)
        self.message_box.setText('Planilha Salva')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = Main()
    widget.show()
    sys.exit(app.exec())
