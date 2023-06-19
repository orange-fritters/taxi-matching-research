from abc import *
from typing import List, Tuple, Dict
import pandas as pd
import numpy as np
from weight_assigning_model import Model, calculate_time_arrival
from scipy.optimize import linear_sum_assignment


class Vehicle():
    id: int
    ETA: int            # 남은 시간 (운행중이지 않으면 0)
    curr_loc: int       # destination_loc이 정해지는 순간 변경됨
    curr_time: int      # 그냥 현재 시간 알려줌 리팩토링할 때 없애도 되는 변수?
    available: bool     # 현재 공차 여부, 근데 ETA가 5 이하이면 True
    working: bool       # 현재 기사님이 일하는지 여부


class Request():
    id: int
    travel_time: int      # 이동한 시간 == 하차 시간 - 탑승 시간
    request_time: int     # 요청 시각
    origin_loc: int       # startpos2
    destination_loc: int  # endpos2


class SimulatorInterface(metaclass=ABCMeta):
    
    def __init__(self,
                 data: pd.DataFrame,
                 total_time: int,
                 time_window: int,
                 tolerance: int = 5) -> None:
        """
        Simulator class for simulation
        """
        self.data: pd.DataFrame = data
        self.requests: Dict[int, Request] = {} # key : ID, value: Request
        self.vehicles: Dict[int, Vehicle] = self.init_make_vehicles() # key : ID, value: Vehicle
        self.waiting_times: Dict[int, int] = {} # key : request ID, value : waiting time
        self.model = Model()
        self.total_time = total_time        # 총합 시간 (첨두 비첨두 따라 다르므로, 단위 : min)
        self.time_window = time_window      # batch interval (단위 : min)
        self.counter = 0                    # self.data에서 현재 추적중인 행
        self.matched_number = 0             # 매칭된 요청의 수(최종 리턴 값)
        self.tolerance = tolerance
        self.log_data = pd.DataFrame(columns=['curr_time', 'request_id', 'waiting_time', 'arrival_time', 'total_time', 'req_loc'])

    def init_make_vehicles(self):
        vehicles = {}
        for veh_id in self.data['no'].unique():
            vehicle = Vehicle()
            vehicle.id = veh_id
            vehicle.ETA = 0
            vehicle.curr_loc = self.data.loc[self.data['no'] == veh_id, 'startposid'].iloc[0]
            vehicle.curr_time = 0
            vehicle.available = True
            vehicle.working = True # TODO : Implement working
            vehicles[veh_id] = vehicle
        return vehicles
    
    def update_vehicle_status(self):
        """
        1. Update Vehicle's ETA by Subtracting Each
        2. Update Vehicle's availability (work started, work ended)

        Variables:
            self.vehicles: list of all vehicles
        Update:
            self.vehicles
        """
        for vehicle in self.vehicles.values():
            vehicle.curr_time += 1
            if vehicle.ETA > 0:
                vehicle.ETA -= 1
            # if vehicle.ETA == 0: <- filter_vehicles에서 이미 available 처리됨

        # TODO : Update Vehicle's availability by work started and ended)
    
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
            self.vehicles[veh_id].available = False
            self.vehicles[veh_id].curr_loc = self.requests[req_id].origin_loc
            del self.requests[req_id]

        for req_id in self.requests: # unmatched requests are in self.requests
            self.waiting_times[req_id] += self.time_window
    
    def _create_request(self, counter):
        req = Request()
        req.id = counter
        req.travel_time = self.data.loc[counter, "endtime"] - self.data.loc[counter, "ridetime"]
        req.request_time = self.data.loc[counter, "desiredtime"]
        req.origin_loc = self.data.loc[counter, "startposid"]
        req.destination_loc = self.data.loc[counter, "endposid"]
        req.arrival_time = 0
        return req

    def update_requests(self, 
                        time: int):
        """
        Update the requests variable and waiting times for some requests time by time 
        Data should be sorted by desiredtime
        """
        df = self.data
        while self.counter < len(df) and df.loc[self.counter, "desiredtime"] == time:
            req = self._create_request(self.counter)
            self.requests[req.id] = req
            self.waiting_times[req.id] = 0
            self.counter += 1
    
    def filter_vehicles(self) -> None:
        """
        Modify self.vehicle's available parameter for current requests
        Args:
            self.requests: list of requests
            self.vehicles: list of all vehicles
        Returns:
            self.vehicles : modified self.vehicles
        """
        for vehicle in self.vehicles.values():
            if not vehicle.available and vehicle.ETA <= self.tolerance:
                vehicle.available = True
                
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
        weight, index_to_id = self.model.assign(self.requests, self.vehicles)
        return weight, index_to_id

    def KM_algorithm(self, 
                     weight: np.array, 
                     index_to_id: Dict) -> List[Tuple]:
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
        vehicle_indices, request_indices = linear_sum_assignment(weight)
        assignments = []
        for vehicle_index, request_index in zip(vehicle_indices, request_indices):
            vehicle_id, request_id = index_to_id[(vehicle_index, request_index)]
            assignments.append((vehicle_id, request_id))

        return assignments

    
    def log(self, 
            matched_pair: List[Tuple]) -> None:
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
        for veh_id, req_id in matched_pair:
            waiting_time = self.waiting_times[req_id]
            arrival_time = calculate_time_arrival(self.vehicles[veh_id].curr_loc, self.requests[req_id].origin_loc)
            total_time = waiting_time + arrival_time
            req_loc = self.requests[req_id].origin_loc
            self.log_data = self.log_data.append({
                'curr_time': self.vehicles[veh_id].curr_time,
                'request_id': req_id,
                'waiting_time': waiting_time,
                'arrival_time': arrival_time,
                'total_time': total_time,
                'req_loc': req_loc
            }, ignore_index=True)
        # TODO: Implement log function to know the distribution of waiting time

    
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
        weight, index_to_id = self.assign_weight()
        matched_pair = self.KM_algorithm(weight, index_to_id)
        self.matched_number += len(matched_pair)
        self.log(matched_pair)
        self.update_vehicle_object(matched_pair)

    
    def simulate(self) -> List[int]:
        """
        Simulate
        """
        for t in range(self.total_time):
            self.update_vehicle_status()
            self.update_requests(t)

            if t % self.time_window == 0 and t != 0:
                self.filter_vehicles()
                self.match()
                print(f"Time : {t}, Matched : {self.matched_number}")
        
        self.log_data.to_csv("log.csv")
        return self.waiting_times # It contains each request's waiting time (log)
