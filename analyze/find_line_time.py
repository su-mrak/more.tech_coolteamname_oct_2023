from uuid import UUID
import numpy as np
import enum
from datetime import time
from datetime import date
from random import randint
import matplotlib.pyplot as plt

from pydantic import Field

from backend.app.schemas.office import Office, OpenHours


# 0: 0-10 mins for waiting, 1: 10-20 min, 2: 20-30 min, 4: 30-50min, 5: >50min;
def generate_prediction_time_for_hours(working_hours: list) -> dict:

    working_hours_list_as_x = np.arange(working_hours[0], working_hours[1], 1)

    coefficient_dict = {}
    for hour in working_hours_list_as_x:
        
        if hour < 11:
            coefficient_dict[hour] = randint(2, 3)
            continue

        if hour >= 12 and hour <= 14:
            coefficient_dict[hour] = randint(2, 3)
            continue

        if hour > 17 and hour < 20:
            coefficient_dict[hour] = randint(2, 3)
            continue

        coefficient_dict[hour] = randint(0, 1)
    
    return coefficient_dict
    

def make_prediction_for_a_day(day: date, working_hours: OpenHours) -> dict:

    opens_at = working_hours.opens_at
    closes_at = working_hours.closes_at
    
    if opens_at != None:
        prediction_for_a_day = generate_prediction_time_for_hours([opens_at, closes_at])

        return prediction_for_a_day


def collect_data_with_main_prediction_for_a_talers_model(taler_model: Office, day) -> dict:
    taler_id = taler_model.id_
    taler_individual_working_hours = taler_model.individual_schedule[day]
    taler_legal_entity_working_hours = taler_model.legal_entity_schedule[day]

    individual_schedule_prediction = make_prediction_for_a_day(day, taler_individual_working_hours)
    entity_schedule_prediction = make_prediction_for_a_day(day, taler_legal_entity_working_hours)

    result = {
        "taler_id": id,
        "individual_schedule_prediction": individual_schedule_prediction,
        "entity_schedule_prediction": entity_schedule_prediction
    }
    return result
