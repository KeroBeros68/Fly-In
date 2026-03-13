from typing import Tuple


class Drone():
    __nb_drones: int = 0

    def __init__(self, drone_id: int, pos: Tuple[int, int]) -> None:
        self.__drone_id: int = drone_id
        self.__pos: Tuple[int, int] = pos
        Drone.__nb_drones += 1

    @property
    def drone_id(self) -> int:
        return self.__drone_id

    @property
    def pos(self) -> Tuple[int, int]:
        return self.__pos

    @pos.setter
    def pos(self, new_pos: Tuple[int, int]) -> None:
        self.__pos = new_pos

    @classmethod
    def get_nb_drones(cls) -> int:
        return cls.__nb_drones

    def __del__(self) -> None:
        Drone.__nb_drones -= 1

    def __repr__(self) -> str:
        return f"Drone(id={self.__drone_id}, pos={self.__pos})"
