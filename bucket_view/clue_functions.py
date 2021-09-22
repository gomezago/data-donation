from datetime import datetime
from utils.bucket_functions import *
import time

# Clue Constants
MENSTRUAL_PAIN_TYPE = 'pain'
C_8 = 1, 0, 0, 0
C_4 = 0, 1, 0, 0
C_2 = 0, 0, 1, 0
C_1 = 0, 0, 0, 1

# Contraceptive Inejection Event
APPLIED = 1

# Contraceptive IUD Event
INSERTED = 0
CHECKED = 1
IUD_RETIRED = 2

# Clue Dict for variable types
mult_values_dict = {
    'pain': ['cramps', 'headache', 'ovulation_pain', 'tender_breasts'],
    'mood': ['happy', 'sensitive', 'sad', 'pms'],
    'sex' : ['protected', 'unprotected', 'high_sex_drive', 'withdrawal'],
    'energy' : ['energized', 'high_energy', 'low_energy', 'exhausted'],
    'craving' : ['sweet_craving', 'salty_craving', 'chocolate_craving', 'carbs_craving'],
    'hair' : ['good_hair', 'bad_hair', 'oily_hair', 'dry_hair'],
    'digestion' : ['great_digestion', 'bloated', 'nauseated', 'gassy'],
    'poop' : ['great_poop', 'diarrhea', 'normal_poop', 'constipated'],
    'skin' : ['good_skin', 'oily_skin', 'acne_skin', 'dry_skin'],
    'mental' : ['focused', 'distracted', 'calm', 'stressed'],
    'motivation' : ['motivated', 'unmotivated', 'productive', 'unproductive'],
    'social' : ['conflict_social', 'supportive_social', 'sociable', 'withdrawn_social'],
    'exercise' : ['running', 'yoga', 'biking', 'swimming'],
    'appointment' : ['ob_gyn_appointment', 'vacation_appointment', 'doctor_appointment', 'date_appointment'],
    'party' : ['drinks_party', 'cigarettes', 'hangover', 'big_night_party'],
    'collection_method': ['tampon_collection_method', 'pad_collection_method','panty_liner_collection_method','menstrual_cup_collection_method'],
    'ailment' : ['cold_flu_ailment', 'injury_ailment', 'allergy_ailment', 'fever_ailment'],
    'medication' : ['pain_medication', 'cold_flu_medication', 'antibiotic_medication', 'antihistamine_medication'],
    'test' : ['ovulation_test_pos', 'ovulation_test_neg', 'pregnancy_test_pos', 'pregnancy_test_neg'], #ID: MENSTRUATION_TEST_EVENT
}

sing_vales_dict = {
    'period' : ['heavy', 'medium', 'light', 'spotting'],
    'sleep' : ['0_to_3_hours', '3_to_6_hours', '6_to_9_hours', '9_or_more_hours'],
    'fluid' : ['creamy', 'egg_white', 'sticky', 'atypical'],
    'ring' : ['removed', 'removed_late', 'replaced', 'replaced_late'],
    'patch': ['removed', 'removed_late', 'replaced', 'replaced_late'],
    'pill' : ['taken', 'missed', 'late', 'double'],
}

bucket_clue_dict = {
    "MENSTRUAL_PAIN_TYPE":'pain',
    "MENSTRUATION_TYPE":'period',
    "SLEEP_DURATION":'sleep',
    "PERSONAL_ENERGY_LEVEL":'energy',
    "HAIR_TYPE":'hair',
    "SEXUAL_ACTIVITY":'sex',
    "EXERCISE_TYPE":'exercise',
    "SKIN_QUALITY":'skin',
    "MENSTRUAL_FLUID_TYPE":'fluid',
    "MOTIVATION_TYPE":'motivation',
    "MENTAL_STATE":'mental',
    "SOCIAL_MOOD":'social',
    "POOP_QUALITY":'poop',
    "MOOD":'mood',
    "WEIGHT":'weight',
    "DIGESTION_QUALITY":'digestion',
    "CRAVINGS":'craving',
    "MENSTRUATION_COLLECTION_METHOD":'collection_method',
    "CONTRACEPTIVE_RING_EVENT":'ring',
    "TEMPERATURE":'bbt',
    "AILMENT_TYPE":'ailment',
    "MENSTRUATION_TEST_EVENT":'test',
    "CONTRACEPTIVE_INJECTION_EVENT":'injection',
    "MEDITATION":'meditation',
    "APPOINTMENT_TYPE":'appointment',
    "SOCIAL_EVENT":'party',
    "CONTRACEPTIVE_PATCH_EVENT":'patch',
    "CONTRACEPTIVE_IUD_EVENT":'iud',
    "TEXT":'tags',
    "MEDICATION_TYPE":'medication',
    "CONTRACEPTIVE_PILL_EVENT":'pill',
}

clue_bucket_dict = {
    'pain' : "MENSTRUAL_PAIN_TYPE",
    'period' : "MENSTRUATION_TYPE",
    'sleep' : "SLEEP_DURATION",
    'energy' : "PERSONAL_ENERGY_LEVEL",
    'hair' : "HAIR_TYPE",
    'sex' : "SEXUAL_ACTIVITY",
    'exercise' : "EXERCISE_TYPE",
    'skin' : "SKIN_QUALITY",
    'fluid' : "MENSTRUAL_FLUID_TYPE",
    'motivation' : "MOTIVATION_TYPE",
    'mental' : "MENTAL_STATE",
    'social' : "SOCIAL_MOOD",
    'poop' : "POOP_QUALITY",
    'mood' : "MOOD",
    'weight' : "WEIGHT",
    'digestion' : "DIGESTION_QUALITY",
    'craving' : "CRAVINGS",
    'collection_method' : "MENSTRUATION_COLLECTION_METHOD",
    'ring' : "CONTRACEPTIVE_RING_EVENT",
    'bbt' : "TEMPERATURE",
    'ailment' : "AILMENT_TYPE",
    'test' : "MENSTRUATION_TEST_EVENT",
    'injection' : "CONTRACEPTIVE_INJECTION_EVENT",
    'meditation' : "MEDITATION",
    'appointment' : "APPOINTMENT_TYPE",
    'party' : "SOCIAL_EVENT",
    'patch' : "CONTRACEPTIVE_PATCH_EVENT",
    'iud' : "CONTRACEPTIVE_IUD_EVENT",
    'tags' : "TEXT",
    'medication' : "MEDICATION_TYPE",
    'pill' : "CONTRACEPTIVE_PILL_EVENT",
}

def read_clue_file(clue_file, choices):

    selected_data = {k: bucket_clue_dict[k] for k in choices}
    new_dict = {}

    for dict_data in clue_file:
        timestamp_date_time = datetime.strptime(dict_data['day'], '%Y-%m-%dT%H:%M:%SZ')
        timestamp_unix = int(time.mktime(timestamp_date_time.timetuple())*1000) # Timestamp in ms
        timestamp_list = [timestamp_unix]

        for k, v in dict_data.items():
            if k in selected_data.values():
                if v and k != 'day':
                    items = v
                    if type(items) != list:
                        items = [items]
                    value = timestamp_list + items
                    if k in new_dict:
                        new_dict[k].append(value)
                    else:
                        new_dict[k] = [value]
    return new_dict

def transform_clue_dict(clue_dict):
    for k, v in clue_dict.items():
        if k in mult_values_dict:
            values = []
            for item in v:
                item = [C_8 if x == mult_values_dict[k][0] else C_4 if x == mult_values_dict[k][1] else
                        C_2 if x == mult_values_dict[k][2] else C_1 if x == mult_values_dict[k][3]
                        else x for x in item]
                if len(item) > 2:
                    items = tuple([sum(x) for x in zip(*item[1:])])
                    values.append([item[0], items[0], items[1], items[2], items[3]])
                else:
                    values.append([item[0], item[1][0], item[1][1], item[1][2], item[1][3]])
            clue_dict[k] = values
        if k in sing_vales_dict:
            values = []
            for item in v:
                values.append([0 if x == sing_vales_dict[k][0] else 1 if x == sing_vales_dict[k][1]
                        else 2 if x == sing_vales_dict[k][2] else 3 if x == sing_vales_dict[k][3]
                        else x for x in item])
            clue_dict[k] = values
        elif k == 'weight':
            values = []
            for item in v:
                if (item[1].get('is_kilogram')):
                    values.append([item[0], item[1].get('weight')])
                else:
                    values.append([item[0], round(item[1].get('weight')/2.2046,2)])
            clue_dict[k] = values
        elif k == 'bbt':
            values = []
            for item in v:
                if item[1].get('is_celsius'):
                    values.append([item[0], item[1].get('temperature')])
                else:
                    values.append([item[0], round(item[1].get('temperature')-32*5/9,2)])
            clue_dict[k] = values
        elif k == 'meditation':
            values = []
            for item in v:
                values.append([item[0], item[1].get('duration_in_minutes')])
            clue_dict[k] = values
        elif k == 'injection':
            values = []
            for item in v:
                values.append([1 if x == "administered" else x for x in item])
            clue_dict[k] = values
        elif k == 'iud':
            values = []
            for item in v:
                values.append([0 if x == "inserted" else 1 if x == "thread_checked"
                else 2 if x == "removed" else x for x in item])
            clue_dict[k] = values
    return clue_dict

def send_clue_data(thingId, data_dict, property_dict, token):
    for k, v in data_dict.items():
        if k in clue_bucket_dict and clue_bucket_dict[k] in property_dict:
            if v:
                update = update_property(thingId, property_dict[clue_bucket_dict[k]], {'values': v}, token)
                print(update)
