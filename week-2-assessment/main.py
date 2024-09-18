# Import necessary modules
import json
import csv
from weather import get_weather
from models.aircraft import Aircraft
from models.pilot import Pilot
from models.target import Target
from files import load_entities, save_to_csv
from scoring import calculate_mission_options, calculate_mission_combinations, display_mission_options, display_mission_combinations

# Display menu options
def display_menu():
    print("\nAir Strike Simulation Menu:")
    print("1. Load Air Strikes from JSON File")
    print("2. Display All Strikes and Results")
    print("3. Save All Strikes to CSV File")
    print("4. Exit")


# Display all missions and their results
def display_all_missions(missions):
    if not missions:
        print("No missions to display.")
        return
    for mission in missions:
        print(f"Aircraft: {mission.aircraft.aircraft_type}, Pilot: {mission.pilot.name}, "
              f"Target: {mission.target.target_type},Weather : {mission.weather}, Result: {mission.result}")


# Main function to run the simulation
def main():
    # 1. Load JSONs
    entities = load_entities()

    # 2. Calculate mission options with score and sort DESC
    mission_options, mission_options_indexes = calculate_mission_options(entities)

    # 3. Display all mission options
    display_mission_options(mission_options)
    
    # 4. Calculate best fit combo and sort it DESC
    # We use the smallest array to be the base for the calculations
    mission_combinations = calculate_mission_combinations(
        mission_options_indexes,
        pow(len(entities['aircrafts']) * len(entities['targets']) * len(entities['pilots']), 3),
        len(entities['pilots'])
    )

    # 5. Print the mission combinations sorted DESC
    display_mission_combinations(entities, mission_combinations)

def menu():
    while True:
        display_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            file_name = input("Enter the JSON file path: ")
            missions.extend(load_air_strikes_from_json(file_name))
        elif choice == "2":
            mission = manually_add_air_strike()
            missions.append(mission)
        elif choice == "3":
            display_all_missions(missions)
        elif choice == "4":
            file_name = input("Enter the CSV file name to save the results: ")
            save_to_csv(missions, file_name)
        elif choice == "5":
            print("Exiting the simulation.")
            break
        else:
            print("Invalid choice. Please try again.")


# Run the simulation
if __name__ == "__main__":
    main()
