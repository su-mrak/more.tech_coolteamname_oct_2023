import calendar
import enum


class WeekdaysRu(str, enum.Enum):
    MONDAY = "пн"
    TUESDAY = "вт"
    WEDNESDAY = "ср"
    THURSDAY = "чт"
    FRIDAY = "пт"
    SATURDAY = "сб"
    SUNDAY = "вс"


weekday_ru_to_int: dict[WeekdaysRu, int] = {
    WeekdaysRu.MONDAY: calendar.MONDAY,
    WeekdaysRu.TUESDAY: calendar.TUESDAY,
    WeekdaysRu.WEDNESDAY: calendar.WEDNESDAY,
    WeekdaysRu.THURSDAY: calendar.THURSDAY,
    WeekdaysRu.FRIDAY: calendar.FRIDAY,
    WeekdaysRu.SATURDAY: calendar.SATURDAY,
    WeekdaysRu.SUNDAY: calendar.SUNDAY,
}

weekdays_ru: list[WeekdaysRu] = [
    WeekdaysRu.MONDAY,
    WeekdaysRu.TUESDAY,
    WeekdaysRu.WEDNESDAY,
    WeekdaysRu.THURSDAY,
    WeekdaysRu.FRIDAY,
    WeekdaysRu.SATURDAY,
    WeekdaysRu.SUNDAY,
]


class Weekdays(str, enum.Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


weekday_en_to_int: dict[Weekdays, int] = {
    Weekdays.MONDAY: calendar.MONDAY,
    Weekdays.TUESDAY: calendar.TUESDAY,
    Weekdays.WEDNESDAY: calendar.WEDNESDAY,
    Weekdays.THURSDAY: calendar.THURSDAY,
    Weekdays.FRIDAY: calendar.FRIDAY,
    Weekdays.SATURDAY: calendar.SATURDAY,
    Weekdays.SUNDAY: calendar.SUNDAY,
}

weekday_int_to_en: dict[int, Weekdays] = {
    value: key for key, value in weekday_en_to_int.items()
}

weekday_ru_to_en: dict[WeekdaysRu, Weekdays] = {
    WeekdaysRu.MONDAY: Weekdays.MONDAY,
    WeekdaysRu.TUESDAY: Weekdays.TUESDAY,
    WeekdaysRu.WEDNESDAY: Weekdays.WEDNESDAY,
    WeekdaysRu.THURSDAY: Weekdays.THURSDAY,
    WeekdaysRu.FRIDAY: Weekdays.FRIDAY,
    WeekdaysRu.SATURDAY: Weekdays.SATURDAY,
    WeekdaysRu.SUNDAY: Weekdays.SUNDAY,
}
