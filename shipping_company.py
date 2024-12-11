from abc import ABC, abstractmethod
from typing import List

class TariffException(Exception):
    """Пользовательское исключение для обработки ошибок, связанных с тарифами"""
    pass

class IPriceStrategy(ABC):
    """Интерфейс для стратегии расчета цены"""
    @abstractmethod
    def calculate_price(self, price: float) -> float:
        pass

class RegularPriceStrategy(IPriceStrategy):
    """Стратегия расчета обычной цены без скидки"""
    def calculate_price(self, price: float) -> float:
        return price

class DiscountPriceStrategy(IPriceStrategy):
    """Стратегия расчета цены со скидкой"""
    def __init__(self, discount_percent: float):
        if not 0 <= discount_percent <= 100:
            raise TariffException("Процент скидки должен быть от 0 до 100")
        self.discount_percent = discount_percent

    def calculate_price(self, price: float) -> float:
        return price * (1 - self.discount_percent / 100)

class ITariff(ABC):
    """Интерфейс для тарифов"""
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_price(self) -> float:
        pass

    @abstractmethod
    def calculate_final_price(self) -> float:
        pass

class BaseTariff(ITariff):
    """Базовый класс тарифа"""
    def __init__(self, name: str, price: float):
        if price <= 0:
            raise TariffException("Цена не может быть отрицательной или нулевой")
        if not name:
            raise TariffException("Название тарифа не может быть пустым")
    
        self.name = name
        self.price = price
        self.discount_percent = 0
        self.price_strategy = RegularPriceStrategy()

    def _update_price_strategy(self):
        if self.discount_percent > 0:
            self.price_strategy = DiscountPriceStrategy(self.discount_percent)
        else:
            self.price_strategy = RegularPriceStrategy()

    def set_discount(self, discount_percent: float):
        """Установить скидку для тарифа"""
        if not 0 <= discount_percent <= 100:
            raise TariffException("Процент скидки должен быть от 0 до 100")
        self.discount_percent = discount_percent
        self._update_price_strategy()

    def get_discount(self) -> float:
        """Получить текущую скидку"""
        return self.discount_percent

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> float:
        return self.price

    def calculate_final_price(self) -> float:
        return self.price_strategy.calculate_price(self.price)

class ShippingCompany:
    """Класс компании грузоперевозок"""
    def __init__(self):
        self.tariffs: List[BaseTariff] = []

    def has_tariff(self, name: str) -> bool:
        """Проверка существования тарифа с таким именем"""
        return any(tariff.get_name() == name for tariff in self.tariffs)

    def get_tariff(self, name: str) -> BaseTariff:
        """Получить тариф по имени"""
        for tariff in self.tariffs:
            if tariff.get_name() == name:
                return tariff
        raise TariffException(f"Тариф с названием '{name}' не найден")

    def add_tariff(self, tariff: BaseTariff) -> None:
        """Добавление нового тарифа"""
        if not isinstance(tariff, BaseTariff):
            raise TariffException("Неверный тип тарифа")
        if self.has_tariff(tariff.get_name()):
            raise TariffException(f"Тариф с названием '{tariff.get_name()}' уже существует")
        self.tariffs.append(tariff)

    def set_tariff_discount(self, name: str, discount_percent: float) -> None:
        """Установить скидку для существующего тарифа"""
        tariff = self.get_tariff(name)
        tariff.set_discount(discount_percent)

    def find_min_price_tariff(self) -> BaseTariff:
        """Поиск тарифа с минимальной стоимостью"""
        if not self.tariffs:
            raise TariffException("Список тарифов пуст")
        return min(self.tariffs, key=lambda x: x.calculate_final_price())

    def get_all_tariffs(self) -> List[BaseTariff]:
        """Получение списка всех тарифов"""
        return self.tariffs.copy()
