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

    def calculate_time(self, loc1: int, loc2: int):
        # TODO : Calculate travel time between two location
        return 1
    
    def calculate_weight(self, vehicle: Vehicle, request: Request):
        # TODO : Calculate weight of vehicle and request
        # time_by_distance = self.calculate_time(vehicle.curr_loc, request.origin_loc)
        time_by_distance = self.calculate_time(1, 2)
        
        # 거리에 따른 시간 + 만약 곧 도착 예정인 차량이라면 남은 시간 + (승객의 대기시간)
        return time_by_distance + vehicle.ETA + (request.requset_time - vehicle.curr_time)
    
    def assign(self, requests: Dict[int, Request], vehicles: Dict[int, Vehicle]):
        matrix = np.zeros((len(self.requests), len(self.vehicles)))
        id_to_index = {}
        for vehicle_id, vehicle in enumerate(vehicles):
            for request_id, request in enumerate(requests):
                weight = self.calculate_weight(vehicle, request)  # Your weight calculation function
                matrix[vehicle_id, request_id] = weight
                id_to_index[(vehicle_id, request_id)] = (vehicle_id, request_id)

        return matrix, id_to_index

