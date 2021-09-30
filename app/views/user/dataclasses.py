from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Coordinates:
    x: Decimal
    y: Decimal


@dataclass
class NeighborsSearchParameters:
    user_id: int
    radius: Decimal
    limit: int
    user_coordinates: Coordinates
