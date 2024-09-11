import csv
import json
from mission import Mission
from aircraft import Aircraft
from pilot import Pilot
from target import Target


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


def load_air_strikes_from_json(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
            missions = []
            for entry in data:
                aircraft = Aircraft(entry["aircraft_type"], 100, 800)  # נתוני מטוס לדוגמה
                pilot = Pilot(entry["pilot_name"], entry["pilot_skill"])
                target = Target(entry["target_type"], entry["target_defense"])
                weather = entry["weather"]  # שימוש במזג אוויר מתוך הקובץ
                mission = Mission(aircraft, pilot, target, weather)
                mission.simulate()
                missions.append(mission)
            return missions
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return []
