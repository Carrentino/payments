from enum import StrEnum


class TransactionType(StrEnum):
    WITHDRAW = 'Вывод'
    DEPOSIT = 'Пополнение'


class TransactionStatus(StrEnum):
    PENDING = 'В ожидании'
    SUCCESS = 'Успешно'
    CANCELLED = 'Отменен'
    ERROR = 'Ошибка'
