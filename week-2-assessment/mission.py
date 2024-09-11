class Mission:
    def __init__(self, aircraft, pilot, target, weather):
        self.aircraft = aircraft
        self.pilot = pilot
        self.target = target
        self.weather = weather
        self.result = None

    def simulate(self):
        import random
        success_threshold = self.pilot.skill_level * 10 - self.target.defense_rating
        if self.weather == "Stormy":
            success_threshold -= 20
        elif self.weather == "Windy":
            success_threshold -= 10

        random_factor = random.randint(1, 100)
        if random_factor <= success_threshold:
            self.result = "Success"
        else:
            self.result = "Failure"