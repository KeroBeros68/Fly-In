class Link():
    def __init__(self, name: str, max_drones: int) -> None:
        self.__name: str = name
        self.__max_drones: int = max_drones

    @property
    def name(self) -> str:
        return self.__name

    @property
    def max_drone(self) -> int:
        return self.__max_drones
