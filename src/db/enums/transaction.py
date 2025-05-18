from enum import StrEnum


class TransactionType(StrEnum):
    WITHDRAW = 'Вывод'
    DEPOSIT = 'Пополнение'
    TRANSFER = 'Перевод'


class TransactionStatus(StrEnum):
    PENDING = 'В ожидании'
    SUCCESS = 'Успешно'
    CANCELLED = 'Отменен'
    ERROR = 'Ошибка'
    RESERVED = 'Зарезервировано'
