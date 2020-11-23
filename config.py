from enum import Enum

TOKEN = '1480743002:AAHnqmxBLxebtfqDGhEIzs-UyGPKD-zsqT0'
db_file = "database.vdb"


class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_ENTER_FULL_NAME = "1"
    S_ENTER_PIN = "2"
    S_ENTER_RELATIONSHIP = "3"
    S_ENTER_NUMBER = '4'
    S_ENTER_PATIENT_FULL_NAME = '5'
    S_ENTER_PATIENT_BIRTHDAY = '6'
    S_ENTER_HOSPITALIZATION_DATE = '7'
    S_ENTER_HOSPITALIZATION_PLACE = '8'