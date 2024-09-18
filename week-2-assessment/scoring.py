import time

def calculate_score(target, aircraft, pilot, targets_max_values):
    weights = {
        "target_distance": 0.2, # aircraft fuel capacity / target distance
        "target_execution_time": 0.2, # aircraft speed
        "target_weather": {
            "_self": 0.2,
            "wind_speed": 0.33,
            "cloud_density": 0.33,
            "forecast": 0.33
        },
        "target_priority": 0.2,
        "pilot_skill": 0.2
    }

    # Example calculation (you can adjust based on your scoring criteria)
    distance_score = 1 - min(target.distance / aircraft.fuel_capacity, 1)
    speed_score = aircraft.speed / 2000  # Normalized speed
    skill_score = pilot.skill_level / 10  # Skill score

    # priority score
    priority_score = target.priority / targets_max_values['priority']

    # Calculate weather score
    wind_score = 1 - min(target.wind_speed / targets_max_values['wind_speed'], 1)
    cloud_score = 1 - min(target.cloud_density / 100, 1)
    if target.forecast == "Clear":
        forecast_score = 1
    elif target.forecast == "Clouds":
        forecast_score = 0.8
    elif target.forecast == "Rain":
        forecast_score = 0.5
    elif target.forecast == "Thunderstorm":
        forecast_score = 0.3
    elif target.forecast == "Snow":
        forecast_score = 0.2

    weather_score = \
        wind_score * weights['target_weather']['wind_speed'] + \
        cloud_score * weights['target_weather']['cloud_density'] + \
        forecast_score * weights['target_weather']['forecast']

    # Total score is a weighted combination of these factors
    return \
        distance_score * weights['target_distance'] + \
        speed_score * weights['target_execution_time'] + \
        weather_score * weights['target_weather']['_self'] + \
        priority_score * weights['target_priority'] + \
        skill_score * weights['pilot_skill']
    

def calculate_mission_options(entities: dict) -> tuple:
    combinations = []
    combinations_indexes = []

    for t_index, target in enumerate(entities['targets']):
        
        for a_index, aircraft in enumerate(entities['aircrafts']):
            
            # Calculate scores for each pilot
            for p_index, pilot in enumerate(entities['pilots']):
                score = calculate_score(target, aircraft, pilot, entities['targets_max_values'])
                combinations.append((target, aircraft, pilot, score))
                
                index_dict = dict()
                index_dict['indexes'] = (t_index, a_index, p_index)
                index_dict['score'] = score
                combinations_indexes.append(index_dict)
    
    # Sort combinations by score in descending order
    return \
        sorted(combinations, key=lambda x: x[3], reverse=True), \
        combinations_indexes


def calculate_mission_combinations(combination_indexes: list, rows: int, cols: int):
    array = []
    array_len = len(combination_indexes)
    
    start_time = time.perf_counter()

    for c1_index in range(array_len):
        for c2_index in range(array_len):
            for c3_index in range(array_len):
                combo_list = [
                    combination_indexes[c1_index]['indexes'],
                    combination_indexes[c2_index]['indexes'],
                    combination_indexes[c3_index]['indexes']
                ]

                if not is_conflict(combo_list):
                    array.append({
                        'indexes': combo_list,
                        'avg_score': 
                            (combination_indexes[c1_index]['score'] +    
                            combination_indexes[c2_index]['score'] +  
                            combination_indexes[c3_index]['score']) / cols})
                    # print(f"No conflict - added {combo_list}")
                # else:
                    # print(f"Conflict - skipped {combo_list}")
    
    # Calculate execution time
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

    sorted_array = sorted(array, key = lambda x: x['avg_score'], reverse=True)

    # Return a sorted list based on the average from highest to lowest
    return sorted_array


def is_conflict(combo_list):
    for i in range(len(combo_list[0])):
        if (combo_list[0][i] == combo_list[1][i] or combo_list[0][i] == combo_list[2][i] or combo_list[1][i] == combo_list[2][i]):
            return True

    return False


def display_mission_options(options):
    for option in options:
        print(f"" + \
            f"{option[0].city.ljust(15)}\t" + \
            f"{str(option[0].priority).ljust(3)}\t" + \
            f"{str(option[0].distance)} km\t" + \
            f"{option[0].forecast}\t" + \
            f"{str(option[0].wind_speed)} km/h\t" + \
            f"{str(option[0].cloud_density)} %\t" + \
            f"{option[1].type.ljust(15)}\t" + \
            f"{option[1].speed} km/h\t" + \
            f"{str(option[1].fuel_capacity).ljust(6)} km\t" + \
            f"{option[2].name.ljust(15)}\t" + \
            f"{str(option[2].skill_level).ljust(3)}\t" + \
            f"{option[3]:.5f}")


# Display mission combinations
# input: entities: dict, combinations: list
# combinations: list of dicts with the following structure: 
# {
#     'indexes': (target_index, aircraft_index, pilot_index),
#     'avg_score': average_score
# }
def display_mission_combinations(entities: dict, combinations: list):
    print(f"Top 50 combinations:")
    previous_score = 0
    similar_score_count = 0
    short_index = 0

    for index, combination in enumerate(combinations[:200]):
        # If the score is the same as the previous one, skip it
        if combination['avg_score'] == previous_score:
            similar_score_count += 1
            continue
        elif previous_score != 0:
            print(f"--- Similar combinations: {similar_score_count}\n")
            short_index += 1
            similar_score_count = 0

        print(f"--- {short_index}. {combination['avg_score']:.10f}---")

        for entity in combination['indexes']:
            print(f"" + \
                f"{entities['targets'][entity[0]].city.ljust(15)}\t" + \
                f"{str(entities['targets'][entity[0]].priority).ljust(3)}\t" + \
                f"{str(entities['targets'][entity[0]].distance)} km\t" + \
                f"{entities['targets'][entity[0]].forecast}\t" + \
                f"{str(entities['targets'][entity[0]].wind_speed)} km/h\t" + \
                f"{str(entities['targets'][entity[0]].cloud_density)} %\t" + \
                f"{entities['aircrafts'][entity[1]].type.ljust(15)}\t" + \
                f"{entities['aircrafts'][entity[1]].speed} km/h\t" + \
                f"{str(entities['aircrafts'][entity[1]].fuel_capacity).ljust(6)} km\t" + \
                f"{entities['pilots'][entity[2]].name.ljust(15)}\t" + \
                f"{str(entities['pilots'][entity[2]].skill_level).ljust(3)}\t")

        previous_score = combination['avg_score']
