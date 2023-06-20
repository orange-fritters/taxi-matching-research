import random
import pandas as pd
import numpy as np
from typing import Dict

class Vehicle():
    id: int
    destination_loc: int
    ETA: int
    curr_loc: int
    curr_time: int
    available: bool
    working: bool


class Request():
    id: int
    travel_time: int      # 이동한 시간 == 하차 시간 - 탑승 시간
    request_time: int     # 요청 시각
    origin_loc: int       # 출발동
    destination_loc: int  # 목적동


class Model:
    def __init__(self, 
                 a : float = 0.1, 
                 b : float = 0.1,
                 peak_dir : str = "data/peak.csv",
                 offpeak_dir : str = "data/offpeak.csv"):
        self.a = a
        self.b = b
        self.peak = pd.read_csv(peak_dir, header=None).to_numpy() * 0.06
        self.offpeak = pd.read_csv(offpeak_dir, header=None).to_numpy() * 0.06

    def calculate_time_arrival(self, 
                               t : int, 
                               loc1: int, 
                               loc2: int):
        if 0 <= t < 180 or 480 <= t < 660:
            return self.peak[loc1, loc2].astype(int)
        else:
            return self.offpeak[loc1, loc2].astype(int)
    
    def calculate_weight(self, 
                         t : int,
                         vehicle: Vehicle, 
                         request: Request):
        # 계산식 : 
        arrival_time = self.calculate_time_arrival(t, vehicle.curr_loc, request.origin_loc)
        # 거리에 따른 시간 + 만약 곧 도착 예정인 차량이라면 남은 시간 + (승객의 대기시간)
        return np.exp(self.a * (arrival_time) / 60 + self.b * (request.request_time - vehicle.curr_time) / 60)
        return np.exp(self.b * (request.request_time - t) )
    
    def assign(self, requests: Dict[int, Request], vehicles: Dict[int, Vehicle]):
        num_of_vehicles = sum([vehicle.available and vehicle.working for vehicle in vehicles.values()])
        matrix = np.zeros((num_of_vehicles, len(requests)))

        index_to_id = {}
        vehicle_idx = 0
        for vehicle in vehicles.values():
            request_time = vehicle.curr_time
            if (not vehicle.available or not vehicle.working):
                continue
            for request_idx, request in enumerate(requests.values()):
                weight = self.calculate_weight(request_time, vehicle, request)  # Your weight calculation function
                matrix[vehicle_idx, request_idx] = weight
                index_to_id[(vehicle_idx, request_idx)] = (vehicle.id, request.id)
            vehicle_idx += 1    

        return matrix, index_to_id
