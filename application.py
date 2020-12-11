# **Tax Calculator** - Asks the user to enter a cost and either a country or state tax.
# It then returns the tax plus the total cost with tax.

import sys
import json
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


class SalesTaxCalculatorUI(QMainWindow):
    """Program's GUI/ the view"""

    def __init__(self, model):
        """Initialize view"""
        super().__init__()
        self._model = model
        # Set main window properties
        self.setWindowTitle("Sales Tax Calculator")
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        # Create display, dropdown, button
        self._create_display()
        self._countries_dropdown(self._model.country_names)
        self._create_button()
        self._result_label()
        self._connect_signals()

    def _create_display(self):
        """Create the display"""
        # Create top label
        self.toplabel = QLabel()
        self.toplabel.setText("Sales Tax Calculator")
        self.toplabel.setFont(QtGui.QFont("Sanserif", 20))
        self.toplabel.setAlignment(Qt.AlignCenter)
        # Add top label to general layout
        self.generalLayout.addWidget(self.toplabel)

        # Create entry box for price
        self.price_enter = QLineEdit()
        self.price_enter.setFont(QtGui.QFont("Sanserif", 12))
        self.price_enter.setFixedHeight(30)
        self.price_enter.setAlignment(Qt.AlignCenter)
        # Label
        self.price_enter_label = QLabel()
        self.price_enter_label.setText("Enter price")
        self.price_enter_label.setFont(QtGui.QFont("Sanserif", 12))
        # Add price box and label to general layout
        self.generalLayout.addWidget(self.price_enter_label)
        self.generalLayout.addWidget(self.price_enter)

        # Create tax rate display and label
        self.tax_rate_display = QLabel()
        self.tax_rate_display.setStyleSheet("background-color : rgb(207,225,255)")
        self.tax_rate_display.setFont(QtGui.QFont("Sanserif", 15))
        self.tax_rate_display.setAlignment(Qt.AlignCenter)
        # Label
        self.tax_rate_label = QLabel()
        self.tax_rate_label.setText("Tax rate % of selected country")
        self.tax_rate_label.setFont(QtGui.QFont("Sanserif", 12))
        # Add to general layout
        self.generalLayout.addWidget(self.tax_rate_label)
        self.generalLayout.addWidget(self.tax_rate_display)

    def _countries_dropdown(self, countries):
        # Create dropdown for countries
        self.country_combobox = QComboBox()
        self.country_combobox.setFont(QtGui.QFont("Sanserif", 12))
        self.country_combobox.addItems(countries)
        # Label
        self.country_label = QLabel()
        self.country_label.setText("Pick country")
        self.country_label.setFont(QtGui.QFont("Sanserif", 12))
        # Add label and dropdown to general layout
        self.generalLayout.addWidget(self.country_label)
        self.generalLayout.addWidget(self.country_combobox)

    def _create_button(self):
        # Create button to calculate tax
        self.button = QPushButton("Calculate Tax")
        self.button.setFont(QtGui.QFont("Sanserif", 13))
        self.button.setStyleSheet("background-color : rgb(207,225,255)")
        self.generalLayout.addWidget(self.button)

    def _result_label(self):
        # Create label to show result
        self.result = QLabel()
        self.result.setText("Total price with tax is ")
        self.result.setFont(QtGui.QFont("Sanserif", 13))
        self.generalLayout.addWidget(self.result)

    def set_result_text(self, text):
        """Set display's text"""
        self.result.setText(f"Total price with tax is {text}")

    def clear_display(self):
        self.set_result_text("")

    def _get_input_country(self):
        user_country = self.country_combobox.currentText()
        return user_country

    def _get_input_price(self):
        """Get price input by user"""
        user_price = self.price_enter.text()
        return int(user_price)

    def _get_tax_rate(self):
        user_tax = self._model.get_country_tax(self._get_input_country())
        self.tax_rate_display.setText(str(user_tax))
        return user_tax

    def _calculate_result(self):
        """Get total price with tax using function in model"""
        self.clear_display()
        result = self._model.final_price(input_price=self._get_input_price(), tax_rate=self._get_tax_rate())
        self.set_result_text(result)

    def _connect_signals(self):
        self.button.clicked.connect(self._calculate_result)


class SalesTaxCalculatorModel:
    """Model to handle operations"""

    def __init__(self):
        with open("country_tax.json", "r") as file_handle:
            self.country_list = json.load(file_handle)
        self.countries = dict(self.country_list)
        self.country_names = self.countries.keys()

    def get_country_tax(self, country):
        if country in self.countries:
            return int(self.countries[country])
        return 0.0

    @staticmethod
    def final_price(input_price, tax_rate):
        total = input_price + (input_price * (tax_rate / 100))
        return total


def main():
    """Main function"""
    # Create an instance of QApplication
    sales_tax_calculator = QApplication(sys.argv)
    # Create instance of model
    model = SalesTaxCalculatorModel()
    # Show program GUI
    view = SalesTaxCalculatorUI(model)
    view.show()
    # Execute program's main loop
    sys.exit(sales_tax_calculator.exec())


if __name__ == '__main__':
    main()
