# Import necessary modules
import json
import csv
from weather import get_weather
from mission import Mission
from aircraft import Aircraft
from pilot import Pilot
from target import Target
from files import load_air_strikes_from_json, save_to_csv

# Display menu options
def display_menu():
    print("\nAir Strike Simulation Menu:")
    print("1. Load Air Strikes from JSON File")
    print("2. Manually Add an Air Strike (with Weather API)")
    print("3. Display All Strikes and Results")
    print("4. Save All Strikes to CSV File")
    print("5. Exit")


# Manually add an air strike with weather API
def manually_add_air_strike():
    aircraft_type = input("Enter aircraft type (e.g., Fighter Jet): ")
    pilot_name = input("Enter pilot name: ")
    pilot_skill = int(input("Enter pilot skill level (1-10): "))
    target_type = input("Enter target type (e.g., Enemy Base): ")
    target_defense = int(input("Enter target defense rating: "))
    city = input("Enter the city for weather conditions: ")

    weather = get_weather(city)
    print(f"Weather in {city}: {weather}")

    aircraft = Aircraft(aircraft_type, 100, 800)  # Example values for fuel and speed
    pilot = Pilot(pilot_name, pilot_skill)
    target = Target(target_type, target_defense)
    mission = Mission(aircraft, pilot, target, weather)
    mission.simulate()
    return mission


# Display all missions and their results
def display_all_missions(missions):
    if not missions:
        print("No missions to display.")
        return
    for mission in missions:
        print(f"Aircraft: {mission.aircraft.aircraft_type}, Pilot: {mission.pilot.name}, "
              f"Target: {mission.target.target_type}, Weather: {mission.weather}, Result: {mission.result}")


# Main function to run the simulation
def main():
    missions = []
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
