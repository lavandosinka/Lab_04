import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QMessageBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QDoubleSpinBox
)
from shipping_company import ShippingCompany, BaseTariff, TariffException

class ShippingCompanyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.company = ShippingCompany()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Система управления тарифами грузоперевозок')
        self.setGeometry(100, 100, 800, 600)

        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Левая панель для добавления тарифов и установки скидок
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # Секция добавления тарифа
        add_group = QWidget()
        add_layout = QVBoxLayout(add_group)
        
        add_layout.addWidget(QLabel('Добавление нового тарифа'))
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Название тарифа')
        add_layout.addWidget(self.name_input)

        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(1.00, 500.00)
        self.price_input.setValue(100.00)
        self.price_input.setPrefix('₽ ')
        add_layout.addWidget(self.price_input)

        add_button = QPushButton('Добавить тариф')
        add_button.clicked.connect(self.add_tariff)
        add_layout.addWidget(add_button)

        left_layout.addWidget(add_group)

        # Секция установки скидки
        discount_group = QWidget()
        discount_layout = QVBoxLayout(discount_group)
        
        discount_layout.addWidget(QLabel('Установка скидки'))
        
        self.discount_name_input = QLineEdit()
        self.discount_name_input.setPlaceholderText('Название тарифа')
        discount_layout.addWidget(self.discount_name_input)

        self.discount_input = QDoubleSpinBox()
        self.discount_input.setRange(0.00, 100.00)
        self.discount_input.setValue(0.00)
        self.discount_input.setSuffix(' %')
        discount_layout.addWidget(self.discount_input)

        discount_button = QPushButton('Установить скидку')
        discount_button.clicked.connect(self.set_discount)
        discount_layout.addWidget(discount_button)

        left_layout.addWidget(discount_group)

        # Кнопка поиска минимального тарифа
        find_min_button = QPushButton('Найти минимальный тариф')
        find_min_button.clicked.connect(self.find_min_tariff)
        left_layout.addWidget(find_min_button)

        left_layout.addStretch()
        layout.addWidget(left_panel)

        # Правая панель со списком тарифов
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        right_layout.addWidget(QLabel('Список тарифов'))
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Название', 'Базовая цена', 'Скидка', 'Итоговая цена'])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        right_layout.addWidget(self.table)

        layout.addWidget(right_panel)

        # Загружаем тарифы при запуске
        self.update_table()

    def add_tariff(self):
        try:
            name = self.name_input.text().strip()
            price = self.price_input.value()
            
            if not name:
                raise TariffException("Название тарифа не может быть пустым")
            
            if self.company.has_tariff(name):
                raise TariffException(f"Тариф с названием '{name}' уже существует")

            tariff = BaseTariff(name, price)
            self.company.add_tariff(tariff)
            
            self.name_input.clear()
            self.price_input.setValue(100.00)
            self.update_table()
            QMessageBox.information(self, 'Успех', 'Тариф успешно добавлен!')
            
        except TariffException as e:
            QMessageBox.warning(self, 'Ошибка', str(e))

    def set_discount(self):
        try:
            name = self.discount_name_input.text().strip()
            discount = self.discount_input.value()

            if not name:
                raise TariffException("Название тарифа не может быть пустым")

            self.company.set_tariff_discount(name, discount)
            
            self.discount_name_input.clear()
            self.discount_input.setValue(0.00)
            self.update_table()
            QMessageBox.information(self, 'Успех', 'Скидка успешно установлена!')
            
        except TariffException as e:
            QMessageBox.warning(self, 'Ошибка', str(e))

    def find_min_tariff(self):
        try:
            min_tariff = self.company.find_min_price_tariff()
            message = (f"Тариф с минимальной стоимостью:\n\n"
                      f"Название: {min_tariff.get_name()}\n"
                      f"Базовая цена: {min_tariff.get_price():.2f} ₽\n"
                      f"Скидка: {min_tariff.get_discount():.2f}%\n"
                      f"Итоговая цена: {min_tariff.calculate_final_price():.2f} ₽")
            QMessageBox.information(self, 'Минимальный тариф', message)
        except TariffException as e:
            QMessageBox.warning(self, 'Ошибка', str(e))

    def update_table(self):
        """Обновление таблицы тарифов"""
        tariffs = self.company.get_all_tariffs()
        self.table.setRowCount(len(tariffs))
        
        for row, tariff in enumerate(tariffs):
            name_item = QTableWidgetItem(tariff.get_name())
            base_price_item = QTableWidgetItem(f"₽ {tariff.get_price():.2f}")
            discount_item = QTableWidgetItem(f"{tariff.get_discount():.1f}%")
            final_price_item = QTableWidgetItem(f"₽ {tariff.calculate_final_price():.2f}")
            
            self.table.setItem(row, 0, name_item)
            self.table.setItem(row, 1, base_price_item)
            self.table.setItem(row, 2, discount_item)
            self.table.setItem(row, 3, final_price_item)

def gui_main():
    app = QApplication(sys.argv)
    window = ShippingCompanyGUI()
    window.show()
    sys.exit(app.exec())
