from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Получить сообщение о данных тренировки"""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR = 60
    action: int
    duration_h: float
    weight_kg: float

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_h = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод get_spent_calories не переопределен '
                                  f'в {self.__class__.__name__}.')

    def show_training_info(self) -> InfoMessage:
        """
        Вернуть информационное сообщение
        о выполненной тренировке.
        """
        return InfoMessage(self.__class__.__name__, self.duration_h,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFFICIENT_CALC_CALORIES_FIRST: float = 18
    COEFFICIENT_CALC_CALORIES_SECOND: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (((self.COEFFICIENT_CALC_CALORIES_FIRST * self.get_mean_speed()
                  - self.COEFFICIENT_CALC_CALORIES_SECOND) * self.weight_kg)
                / self.M_IN_KM * self.duration_h * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFFICIENT_CALC_CALORIES_FIRST: float = 0.035
    COEFFICIENT_CALC_CALORIES_SECOND: float = 0.029
    height_sm: float

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_sm = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFFICIENT_CALC_CALORIES_FIRST * self.weight_kg
                 + (self.get_mean_speed() ** 2 // self.height_sm)
                 * self.COEFFICIENT_CALC_CALORIES_SECOND * self.weight_kg)
                * self.duration_h * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFFICIENT_CALC_CALORIES_FIRST: float = 1.1
    COEFFICIENT_CALC_CALORIES_SECOND: float = 2
    length_pool_m: float
    count_pool: int

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        return (self.length_pool_m * self.count_pool
                / self.M_IN_KM / self.duration_h)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.COEFFICIENT_CALC_CALORIES_FIRST)
                * self.COEFFICIENT_CALC_CALORIES_SECOND * self.weight_kg)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_dict: Dict[str: Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in workout_dict:
        return workout_dict[workout_type](*data)
    raise ValueError(f'Неизвестный код тренировки: {workout_type}')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
