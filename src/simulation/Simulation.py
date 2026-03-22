from src.simulation.drone.Drone import Drone


class Simulation():
    def __init__(self):
        self.drone_list: list[Drone] = []

    def start(self):
        self.drone_list = []
        for nb in range(nb_drone):
            self.drone_list.append(Drone(nb + 1, start_pos))
        self.logger.info("All drones initialized")