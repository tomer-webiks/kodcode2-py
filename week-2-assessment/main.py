def display_menu():
    print("\nAir Strike Simulation Menu:")
    print("1. Load Air Strikes from JSON File")
    print("2. Manually Add an Air Strike (with Weather API)")
    print("3. Display All Strikes and Results")
    print("4. Save All Strikes to CSV File")
    print("5. Exit")


def manually_add_air_strike():
    aircraft_type = input("Enter aircraft type (e.g., Fighter Jet): ")
    pilot_name = input("Enter pilot name: ")
    pilot_skill = int(input("Enter pilot skill level (1-10): "))
    target_type = input("Enter target type (e.g., Enemy Base): ")
    target_defense = int(input("Enter target defense rating: "))
    city = input("Enter the city for weather conditions: ")

    weather = get_weather(city)  # Get weather using the API

    print(f"Weather in {city}: {weather}")

    aircraft = Aircraft(aircraft_type, 100, 800)  # Example values for fuel and speed
    pilot = Pilot(pilot_name, pilot_skill)
    target = Target(target_type, target_defense)
    mission = Mission(aircraft, pilot, target, weather)
    mission.simulate()
    return mission