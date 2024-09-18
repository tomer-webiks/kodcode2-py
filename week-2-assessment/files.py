import csv
import json
import os
import math
from models.aircraft import Aircraft
from models.pilot import Pilot
from models.target import Target
from weather import get_lat_lon, get_weather, haversine_distance


def save_to_csv(missions, file_name):
    try:
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Aircraft Type", "Pilot Name", "Pilot Skill", "Target Type", "Target Defense", "Weather", "Result"])
            for mission in missions:
                writer.writerow([mission.aircraft.aircraft_type, mission.pilot.name, mission.pilot.skill_level,
                                 mission.target.target_type, mission.target.defense_rating, mission.weather, mission.result])
        print(f"Saved {len(missions)} missions to {file_name}.")
    except Exception as e:
        print(f"Error saving to CSV: {e}")


def load_entities():
    try:
        entities = dict()
        base_path = os.path.dirname(__file__)
        with open(os.path.join(base_path, 'data', 'aircrafts.json'), 'r') as file:
            data = json.load(file)
            entities['aircrafts'] = []

            for entry in data:
                aircraft = Aircraft(entry["type"], entry["fuel_capacity"], entry["speed"])  # נתוני מטוס לדוגמה
                entities['aircrafts'].append(aircraft)

        with open(os.path.join(base_path, 'data', 'pilots.json'), 'r') as file:
            data = json.load(file)
            entities['pilots'] = []

            for entry in data:
                pilot = Pilot(entry["name"], entry["skill"])  # נתוני מטוס לדוגמה
                entities['pilots'].append(pilot)

        with open(os.path.join(base_path, 'data', 'targets.json'), 'r') as file:
            data = json.load(file)
            entities['targets'] = []
            entities['targets_max_values'] = dict()

            # 0. Get lon/lat for Haifa
            (origin_lon, origin_lat) = get_lat_lon("Haifa")

            for index, entry in enumerate(data):
                city = entry["city"]

                # 1. Make API call to get Lon and Lat
                (target_lon, target_lat) = get_lat_lon(city)

                # 2. Calculate distance between Haifa and target
                distance_km = haversine_distance(origin_lon, origin_lat, target_lon, target_lat)
                print(f"- Called Weather API for {city}, received {target_lon}, {target_lat}.")

                # 3. Make API call to get weather forecast
                (forecast, wind_speed, cloud_density) = get_weather(city)

                # Finally create the object and populate with all information
                target = Target(entry["city"], entry["priority"], distance_km, forecast, wind_speed, cloud_density)  # נתוני מטוס לדוגמה
                entities['targets'].append(target)

                # 4. Save max values for scoring
                if (index == 0 or entities['targets'][index].priority > entities['targets_max_values']['priority']):
                    entities['targets_max_values']['priority'] = entities['targets'][index].priority

                if (index == 0 or entities['targets'][index].wind_speed > entities['targets_max_values']['wind_speed']):
                    entities['targets_max_values']['wind_speed'] = entities['targets'][index].wind_speed

        return entities
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return []