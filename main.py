from shipping_company import ShippingCompany
from shipping_functions import (
    add_tariff,
    set_tariff_discount,
    show_all_tariffs,
    find_min_price_tariff
)


def print_menu():
    print("\n=== Система управления тарифами грузоперевозок ===")
    print("1. Добавить новый тариф")
    print("2. Установить скидку на существующий тариф")
    print("3. Показать все тарифы")
    print("4. Найти тариф с минимальной стоимостью")
    print("0. Выход")
    print("=============================================")

def main():
    company = ShippingCompany()
    
    while True:
        print_menu()
        choice = input("Выберите действие (0-4): ")
        
        if choice == "1":
            add_tariff(company)
        elif choice == "2":
            set_tariff_discount(company)
        elif choice == "3":
            show_all_tariffs(company)
        elif choice == "4":
            find_min_price_tariff(company)
        elif choice == "0":
            print("\nСпасибо за использование программы!")
            break
        else:
            print("\nОшибка: Неверный выбор. Пожалуйста, выберите число от 0 до 4.")

if __name__ == "__main__":
    main()
