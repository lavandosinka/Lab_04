from abc import ABC, abstractmethod
from typing import List, Optional
from database import Database

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
    def __init__(self, name: str, price: float, discount_percent: float = 0):
        if price <= 0:
            raise TariffException("Цена не может быть отрицательной или нулевой")
        if not name:
            raise TariffException("Название тарифа не может быть пустым")
    
        self.name = name
        self.price = price
        self.discount_percent = discount_percent
        self._update_price_strategy()

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
        self.db = Database()

    def has_tariff(self, name: str) -> bool:
        """Проверка существования тарифа с таким именем"""
        tariffs = self.db.get_all_tariffs()
        return any(tariff[0] == name for tariff in tariffs)

    def get_tariff(self, name: str) -> Optional[BaseTariff]:
        """Получить тариф по имени"""
        tariffs = self.db.get_all_tariffs()
        for tariff_data in tariffs:
            if tariff_data[0] == name:
                return BaseTariff(tariff_data[0], float(tariff_data[1]), float(tariff_data[2]))
        raise TariffException(f"Тариф с названием '{name}' не найден")

    def add_tariff(self, tariff: BaseTariff) -> None:
        """Добавление нового тарифа"""
        if not isinstance(tariff, BaseTariff):
            raise TariffException("Неверный тип тарифа")
        
        if self.has_tariff(tariff.get_name()):
            raise TariffException(f"Тариф с названием '{tariff.get_name()}' уже существует")
        
        success = self.db.add_tariff(tariff.get_name(), tariff.get_price())
        if not success:
            raise TariffException("Ошибка при добавлении тарифа в базу данных")

    def set_tariff_discount(self, name: str, discount_percent: float) -> None:
        """Установка скидки для тарифа"""
        if not self.has_tariff(name):
            raise TariffException(f"Тариф с названием '{name}' не найден")
        
        if not 0 <= discount_percent <= 100:
            raise TariffException("Процент скидки должен быть от 0 до 100")
        
        success = self.db.set_tariff_discount(name, discount_percent)
        if not success:
            raise TariffException("Ошибка при установке скидки в базе данных")

    def get_all_tariffs(self) -> List[BaseTariff]:
        """Получить список всех тарифов"""
        tariffs_data = self.db.get_all_tariffs()
        return [BaseTariff(name, float(price), float(discount)) 
                for name, price, discount in tariffs_data]

    def find_min_price_tariff(self) -> Optional[BaseTariff]:
        """Найти тариф с минимальной стоимостью"""
        min_tariff = self.db.get_min_price_tariff()
        if min_tariff:
            return BaseTariff(min_tariff[0], float(min_tariff[1]), float(min_tariff[2]))
        return None
