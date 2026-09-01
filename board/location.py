from enum import Enum

class Location(Enum):
    NONE = (0, 0)
    CORNER = (1, 4)
    EDGE = (5, 9)
    
    @classmethod
    def from_number(cls, number: int):
        for group in cls:
            low, high = group.value
            if low <= number <= high:
                return group
        return Location.NONE