import abc
import numpy as np


class RecommendationCenter:
    __metaclass__ = abc.ABCMeta

    def __init__(self, env, charging_stations, cars, capacity, number_of_fast_chargers):
        self.env = env
        self.charging_stations = charging_stations
        self.cars = cars
        self.capacity = capacity
        self.number_of_fast_chargers = number_of_fast_chargers
        self.future_cs_arrivals = []
        self.future_cs_departures = []
        self.future_fast_spots_arrivals = []
        self.future_fast_spots_departures = []
        self.cars_arriving_list = []
        self.cars_arriving_fast_spots_list = []
        self.waiting_time_per_cs = np.zeros(len(charging_stations))
        self.charging_time_per_cs = np.zeros(len(charging_stations))
        self.number_of_chargings_per_cs = np.zeros(len(charging_stations))
        for i in range(len(charging_stations)):
            self.future_cs_arrivals.append([])#要抵达的
            self.future_cs_departures.append([])#要离开的
            self.future_fast_spots_arrivals.append([])#快充桩要到的
            self.future_fast_spots_departures.append([])#快充桩要离开的
            self.cars_arriving_list.append([])
            self.cars_arriving_fast_spots_list.append([])


    @abc.abstractmethod
    def recommend_charging_station(self, car):
        """
        每一个继承这个类（不同推荐策略）重写这个函数
        """
        return

    def get_cs_occupation(self, cs_number, time):
        """
        预测给定时间给定充电站的车辆数情况
        """
        occupation = len([x for x in self.future_cs_arrivals[cs_number] if x <= time]) - len([x for x in self.future_cs_departures[cs_number] if x < time])
        return occupation if occupation >= 0 else 0

    def get_fast_spot_occupation(self, cs_number, time):
        """
        预测给定时间给定站点快充桩的使用情况
        """
        occupation = len([x for x in self.future_fast_spots_arrivals[cs_number] if x <= time]) - len([x for x in self.future_fast_spots_departures[cs_number] if x < time])
        return occupation if occupation >= 0 else 0

    def get_cs_arrival_and_departure_list(self, cs_number, time):
        """
        给定时间该站点预测的车辆到达和离开的时间
        """
        departures = [x for x in self.future_cs_departures[cs_number] if x < time]
        return [x for x in self.future_cs_arrivals[cs_number] if x <= time and x not in departures]

    def get_fast_spots_arrival_and_departure_list(self, cs_number, time):
        """
        给定时间该站点预测的车辆到达离开快充桩的时间
        """
        departures = [x for x in self.future_fast_spots_departures[cs_number] if x < time]
        return [x for x in self.future_fast_spots_arrivals[cs_number] if x <= time and x not in departures]

    def add_charging_to_cs(self, cs_number):
        """
        给该站点增加一个正在充电的车
        """
        self.number_of_chargings_per_cs[cs_number] += 1

    def add_charging_time_to_cs(self, cs_number, time):
        """
        增加该站点充电的时间
        """
        self.charging_time_per_cs[cs_number] += time

    def add_waiting_time_to_cs(self, cs_number, time):
        """
        增加该站点的等待时间
        """
        self.waiting_time_per_cs[cs_number] += time

    def get_avg_charging_time_for_cs(self, cs_number):
        """
        获取该站点的平均充电时间
        """
        return self.charging_time_per_cs[cs_number] / (self.number_of_chargings_per_cs[cs_number] + 1)

    def get_avg_waiting_time_for_cs(self, cs_number):
        """
        获取该站点的平均等待时间
        """
        return self.waiting_time_per_cs[cs_number] / (self.number_of_chargings_per_cs[cs_number] + 1)







