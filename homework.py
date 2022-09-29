from typing import List, Union
from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE_TEMPLATE = ('Тип тренировки: {training_type}; '
                        'Длительность: {duration:.3f} ч.; '
                        'Дистанция: {distance:.3f} км; '
                        'Ср. скорость: {speed:.3f} км/ч; '
                        'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE_TEMPLATE.format(**asdict(self))

# class InfoMessage:
#     """Информационное сообщение о тренировке."""

#     def __init__(self,
#                  training_type: str,
#                  duration: float,
#                  distance: float,
#                  speed: float,
#                  calories: float) -> None:
#         self.training_type = training_type
#         self.duration = duration
#         self.distance = distance
#         self.speed = speed
#         self.calories = calories

#     def get_message(self) -> str:
#         return (f'Тип тренировки: {self.training_type}; '
#                 f'Длительность: {self.duration:.3f} ч.; '
#                 f'Дистанция: {self.distance:.3f} км; '
#                 f'Ср. скорость: {self.speed:.3f} км/ч; '
#                 f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    M_IN_HOUR = 60
    CALORIE_MULTIPLIER = 18
    CALORIE_MULTIPLIER_2 = 0.029
    LINEAR_SHIFT = 20

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('You should implenet this '
                                  'method in yor child class')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = ((self.CALORIE_MULTIPLIER * self.get_mean_speed()
                          - self.LINEAR_SHIFT)
                          * self.weight / self.M_IN_KM
                          * (self.duration * self.M_IN_HOUR))
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIE_MULTIPLIER = 0.035

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # coeff_calorie_1 = 0.035
        # coeff_calorie_2 = 0.029
        return ((self.CALORIE_MULTIPLIER * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.CALORIE_MULTIPLIER_2 * self.weight)
                * (self.duration * self.M_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIE_MULTIPLIER = 1.1
    CALORIE_MULTIPLIER_2 = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # coeff_calorie_1 = 1.1
        # coeff_calorie_2 = 2
        return ((self.get_mean_speed() + self.CALORIE_MULTIPLIER)
                * self.CALORIE_MULTIPLIER_2
                * self.weight)


def read_package(workout_type: str, data: List[Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""

    available_training = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in available_training:
        return available_training[workout_type](*data)
    else:
        raise ValueError("Неизвестный тип тренировки")


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
