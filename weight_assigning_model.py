import numpy as np
from typing import TypedDict, Dict, List

class Vehicle(TypedDict):
    id: int
    destination_loc: int
    ETA: int
    curr_loc: int
    curr_time: int
    available: bool
    working: bool


class Request(TypedDict):
    id: int
    travel_time: int      # 이동한 시간 == 하차 시간 - 탑승 시간
    request_time: int     # 요청 시각
    origin_loc: int       # 출발동
    destination_loc: int  # 목적동

class Model:
    def __init__(self) -> None:
        pass

    def assign(self, requests: Dict[int, Request], vehicles: Dict[int, Vehicle]) -> np.array:
        # TODO: For each requests, assign a weight for each vehicle
        # Make a matrix of weights (request X vehicle)
        # CAUTION: Keep track of the order of requests and vehicles
        return np.outer()
