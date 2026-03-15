from typing import Tuple


class Drone():
    """
    Representation of a delivery Drone moving across the map.

    Attributes:
        drone_id (int): A unique identifier for the drone.
        pos (Tuple[int, int]): Tuple for (x, y) coordinates of the drone.
    """

    __nb_drones: int = 0

    def __init__(self, drone_id: int, pos: Tuple[int, int]) -> None:
        """
        Initializes a drone's id and base placement.

        Args:
            drone_id (int): Distinct ID assigned sequentially.
            pos (Tuple[int, int]): Initial (x, y) coordinates.
        """
        self.__drone_id: int = drone_id
        self.__pos: Tuple[int, int] = pos
        Drone.__nb_drones += 1

    @property
    def drone_id(self) -> int:
        """
        Gets the drone ID.

        Returns:
            int: The unique identifier.
        """
        return self.__drone_id

    @property
    def pos(self) -> Tuple[int, int]:
        """
        Gets the drone's position.

        Returns:
            Tuple[int, int]: The logical (x, y) coordinate.
        """
        return self.__pos

    @pos.setter
    def pos(self, new_pos: Tuple[int, int]) -> None:
        """
        Sets the position.

        Args:
            new_pos (Tuple[int, int]): Target new coordinates.
        """
        self.__pos = new_pos

    @classmethod
    def get_nb_drones(cls) -> int:
        """
        Retrieves the global count of instantiated Drone objects.

        Returns:
            int: The current drone count.
        """
        return cls.__nb_drones

    def __del__(self) -> None:
        """
        Decrements the global drones count.
        """
        Drone.__nb_drones -= 1

    def __repr__(self) -> str:
        """
        Returns a string summarizing Drone state properties.

        Returns:
            str: Identifier info with coordinate formatting.
        """
        return f"Drone(id={self.__drone_id}, pos={self.__pos})"
