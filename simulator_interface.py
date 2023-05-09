from abc import *
from typing import List, Tuple, TypedDict
import pandas as pd
import numpy as np
from weight_assigning_model import Model


class Vehicle(TypedDict):
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
        self.order: List[Request] = ...
        self.vehicles: List[Vehicle] = ...
        self.waiting_times: List[int] = ...
        self.model = Model()
        self.total_time = total_time        # 총합 시간 (첨두 비첨두 따라 다르므로)
        self.time_window = time_window      # batch interval

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

    @abstractmethod
    def update_order(self,
                     data: pd.DataFrame,
                     time: int) -> None:
        """
        Update the order variable time by time
        """
        self.order = ...

    @abstractmethod
    def filter_vehicles(self) -> None:
        """
        Modify self.vehicle's available parameter for current orders
        Args:
            self.order: list of requests
            self.vehicles: list of all vehicles
        Returns:
            self.vehicles : modified self.vehicles
        """
        pass


    @abstractmethod
    def assign_weight(self) -> np.array:
        """
        Using the model, return the weight
        Only use 
        Args:
            self.order: list of requests
            self.vehicles: list of all vehicles
        Returns:
            weight : modified self.vehicles
        """
        weight: np.array = self.model.assign()
        return weight

    @abstractmethod
    def KM_algorithm(self, weight: np.array) -> List[Tuple]:
        """
        KM Algorithm
        Args:
            weight: np.array
        Variables:
            self.vehicles
            self.order
        Returns:
            matched_pair : List[Tuple] = ...  # Tuple : (veh_idx, request_id)
        """
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
        self.watiting_times = ...

    @abstractmethod
    def match(self, batch, match) -> None:
        """
        Conduct matching process
        Variable:
            self.vehicles
            self.order
        Update:
            self.vehicles
            self.order
        """
        weight = self.assign_weight()
        matched_pair = self.KM_algorithm(weight=weight)
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
            self.update_order(self.data, t)
            if (tmp < self.time_window):
                tmp += 1
            else:
                self.filter_vehicles()
                self.match()
                tmp = 0
        return self.waiting_times
