from shipping_company import ShippingCompany, BaseTariff, TariffException


def input_float(prompt: str, min_value: float = 0, max_value: float = 200) -> float:
    """
    Ввод числа с проверкой.
    :param prompt: сообщение для ввода
    :param min_value: минимальное допустимое значение (если указано)
    :param max_value: максимальное допустимое значение (если указано)
    :return: введенное число
    """
    while True:
        try:
            value = float(input(prompt))
            if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                print(f"Ошибка: Введите число от {min_value} до {max_value}.")
                continue
            return value
        except ValueError:
            print("Ошибка: Введите числовое значение.")

def add_tariff(company: ShippingCompany):
    print("\n--- Добавление нового тарифа ---")
    while True:
        name = input("Введите название тарифа: ").strip()
        if not name:
            print("Ошибка: Название тарифа не может быть пустым.")
            continue
        if company.has_tariff(name):
            print(f"Ошибка: Тариф с названием '{name}' уже существует.")
            continue
        break

    price = input_float("Введите цену (больше 0 и меньше 1000): ", min_value=0.01, max_value=1000)
    
    try:
        tariff = BaseTariff(name, price)
        company.add_tariff(tariff)
        print("Тариф успешно добавлен!")
    except TariffException as e:
        print(f"Ошибка: {e}")

def set_tariff_discount(company: ShippingCompany):
    print("\n--- Установка скидки на существующий тариф ---")
    
    # Показываем список существующих тарифов
    tariffs = company.get_all_tariffs()
    if not tariffs:
        print("Ошибка: Нет доступных тарифов.")
        return

    print("\nСписок доступных тарифов:")
    for i, tariff in enumerate(tariffs, 1):
        print(f"{i}. {tariff.get_name()} (текущая скидка: {round(tariff.get_discount(), 2)}%)")

    while True:
        name = input("\nВведите название тарифа для установки скидки: ").strip()
        if not name:
            print("Ошибка: Название тарифа не может быть пустым.")
            continue
        if not company.has_tariff(name):
            print(f"Ошибка: Тариф с названием '{name}' не найден.")
            continue
        break

    discount = input_float("Введите процент скидки (0-100): ", min_value=0, max_value=100)
    
    try:
        company.set_tariff_discount(name, discount)
        print("Скидка успешно установлена!")
    except TariffException as e:
        print(f"Ошибка: {e}")

def show_all_tariffs(company: ShippingCompany):
    print("\n--- Список всех тарифов ---")
    tariffs = company.get_all_tariffs()
    if not tariffs:
        print("Список тарифов пуст.")
        return
    
    for i, tariff in enumerate(tariffs, 1):
        print(f"{i}. Название: {tariff.get_name()}")
        print(f"   Базовая цена: {tariff.get_price():.2f} руб.")
        print(f"   Скидка: {tariff.get_discount():.2f}%")
        print(f"   Итоговая цена: {tariff.calculate_final_price():.2f} руб.")
        print("   ----------------------")

def find_min_price_tariff(company: ShippingCompany):
    print("\n--- Поиск тарифа с минимальной стоимостью ---")
    try:
        min_tariff = company.find_min_price_tariff()
        print(f"Найден тариф с минимальной стоимостью:")
        print(f"Название: {min_tariff.get_name()}")
        print(f"Базовая цена: {min_tariff.get_price():.2f} руб.")
        print(f"Скидка: {min_tariff.get_discount():.2f}%")
        print(f"Итоговая цена: {min_tariff.calculate_final_price():.2f} руб.")
    except TariffException as e:
        print(f"Ошибка: {e}")
