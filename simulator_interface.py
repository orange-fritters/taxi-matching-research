from abc import *
from typing import List, Tuple, TypedDict, Dict
import pandas as pd
import numpy as np
from weight_assigning_model import Model
from scipy.optimize import linear_sum_assignment


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


class SimulatorInterface(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self,
                 total_time: int,
                 time_window: int) -> None:
        """
        Simulator class for simulation
        """
        self.data: pd.DataFrame = ...
        self.requests: Dict[int, Request] = ... # key : ID, value: Request
        self.vehicles: Dict[int, Vehicle] = ... # key : ID, value: Vehicle
        self.waiting_times: Dict[int, int] = ... # key : request ID, value : waiting time
        self.model = Model()
        self.total_time = total_time        # 총합 시간 (첨두 비첨두 따라 다르므로, 단위 : min)
        self.time_window = time_window      # batch interval (단위 : min)
        self.counter = 0                    # self.data에서 현재 추적중인 행
        self.matched_number = 0             # 매칭된 요청의 수(최종 리턴 값)

    @abstractmethod
    def update_vehicle_status(self):
        """
        1. Update Vehicle's ETA by Subtracting Each
        2. Update Vehicle's availability (work started, work ended)

        Variables:
            self.vehicles: list of all vehicles
        Update:
            self.vehicles
        """
        for vehicle in self.vehicles:
            if vehicle.ETA > 0:
                vehicle.ETA -= 1
            # if vehicle.ETA == 0: <- filter_vehicles에서 이미 available 처리됨

        # TODO : Update Vehicle's availability by work started and ended)

    @abstractmethod
    def update_vehicle_object(self,
                              matched_pair: List[Tuple]):
        """
        1. Update Vehicle's Destination 
        2. Set Vehicle's ETA by Request's travel_time
        3. Remove Processed Request
        4. For Unmatched Requests, Update waiting time

        Args:
          matched_pair
        Variables: 
          self.requests
          self.vehicles
        Update:
          self.requests
          self.vehicles
        """
        for veh_id, req_id in matched_pair:
            self.vehicles[veh_id].destination_loc = self.requests[req_id].destination_loc
            self.vehicles[veh_id].ETA = self.requests[req_id].travel_time
            del self.requests[req_id]

        for req_id in self.requests: # unmatched requests are in self.requests
            self.waiting_times[req_id] += self.time_window


    @abstractmethod
    def update_requests(self,
                     time: int) -> None:
        """
        Update the requests variable and waiting times for some requests time by time 
        """
        data = self.data
        while data.loc[self.counter, "희망일시"] <= time:
            req = Request()
            req.id = self.counter
            req.travel_time = data.loc[self.counter, "하차시간"] - data.loc[self.counter, "탑승시간"]
            req.request_time = data.loc[self.counter, "희망일시"]
            req.origin_loc = data.loc[self.counter, "출발동"]
            req.destination_loc = data.loc[self.counter, "목적동"]
            self.requests[req.id] = req
            self.waiting_times[req.id] = 0
            self.counter += 1


    @abstractmethod
    def filter_vehicles(self) -> None:
        """
        Modify self.vehicle's available parameter for current requests
        Args:
            self.requests: list of requests
            self.vehicles: list of all vehicles
        Returns:
            self.vehicles : modified self.vehicles
        """
        for vehicle in self.vehicles.items():
            if not vehicle.available and vehicle.ETA <= 5:
                vehicle.available = True
                

    @abstractmethod
    def assign_weight(self) -> np.array:
        """
        Using the model, return the weight
        Only use 
        Args:
            self.requests: dict of requests
            self.vehicles: dict of all vehicles
        Returns:
            weight : modified self.vehicles
        """
        weight: np.array = self.model.assign(self.requests, self.vehicles)
        return weight

    @abstractmethod
    def KM_algorithm(self, weight: np.array) -> List[Tuple]:
        """
        KM Algorithm
        Args:
            weight: np.array
        Variables:
            self.vehicles
            self.requests
        Returns:
            matched_pair : List[Tuple] = ...  # Tuple : (veh_id, request_id)
        """
        row_ind, col_ind = linear_sum_assignment(weight)
        # TODO : Implement KM Algorithm
        # weight의 row에 request, col에 vehicle을 배치할 것이므로
        # col_ind가 각 request별 배정된 vehicle의 index가 될 것임

        matched_pair: List[Tuple] = ...  # Tuple : (veh_idx, request_id)
        return matched_pair

    @abstractmethod
    def log(self, matched_pair: List[Tuple]) -> None:
        """
        Log waiting time
        Args:
            matched_pair: List[Tuple] = ...  # Tuple : (veh_idx, request_id)
        Variable:
            self.waiting_time
        Update:
            self.waiting_time
        Raises:
            KeyError: Raises an exception.
        """
        self.waiting_times = ...

    @abstractmethod
    def match(self) -> None:
        """
        Conduct matching process
        Variable:
            self.vehicles
            self.requests
        Update:
            self.vehicles
            self.requests
        """
        weight = self.assign_weight()
        matched_pair = self.KM_algorithm(weight=weight)
        self.matched_number += len(matched_pair)
        self.log(matched_pair=matched_pair)
        self.update_vehicle_object(matched_pair=matched_pair)

    @abstractmethod
    def simulate(self) -> List[int]:
        """
        Simulate
        """
        tmp: int = 0
        for t in range(self.total_time):
            self.update_vehicle_status()
            self.update_requests(t)
            if (tmp < self.time_window):
                tmp += 1
            else:
                self.filter_vehicles()
                self.match()
                tmp = 0
        return self.waiting_times

