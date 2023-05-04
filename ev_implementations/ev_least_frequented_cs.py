import random

from ev_implementations.ev_simulation_base import BaseEV
"""
选择使用频率最低的，同时考虑到车辆距离该充电站的距离，
如果距离相同，就选择充电站车辆数量更少的一个
"""
class EVLeastFrequented(BaseEV):
    def set_charging_station_as_destination(self):
        selected_charging_station = None
        selected_charging_station_distance = None
        selected_charging_station_queue_size = None
        selected_charging_station_cars = None
        found_free_spot = False

        # 计算每个充电站与当前电动汽车的距离和该充电站当前的停车数量，并选择停车数量最少的充电站。
        # 如果有多个充电站停车数量相同，则选择距离更近的充电站。
        for charging_station in self.charging_stations:
            if self.car_number == 1:
                print("FCASQ FREE ", charging_station.charging_station_number, charging_station.get_number_of_free_spots(), charging_station.get_queue_size())
            x, y = charging_station.get_location()
            distance = self.calculate_distance(x, y) + (abs(self.destination[0] - x) + abs(self.destination[1] - y))
            cars_currently = charging_station.get_number_of_cars()

            if selected_charging_station is None or cars_currently < selected_charging_station_cars or (selected_charging_station_cars == cars_currently and distance < selected_charging_station_distance):
                selected_charging_station = charging_station
                selected_charging_station_distance = distance
                selected_charging_station_cars = cars_currently

        nearest_charging_station = None
        nearest_charging_station_distance = None

        # 计算每个充电站与电动汽车目的地的距离，并选择距离最近的充电站。
        for charging_station in self.charging_stations:
            nearest_x, nearest_y = charging_station.get_location()
            distance = self.calculate_distance(nearest_x, nearest_y) + (abs(self.destination[0] - nearest_x) + abs(self.destination[1] - nearest_y))
            if nearest_charging_station is None or distance < nearest_charging_station_distance:
                nearest_charging_station = charging_station
                nearest_charging_station_distance = distance

        # 如果前两个步骤中选择的充电站不同，则根据接受度参数随机选择使用哪个充电站作为目的地。
        if selected_charging_station != nearest_charging_station:
            if random.randint(0, 100) > self.acceptance * 100:
                selected_charging_station = nearest_charging_station

        if self.car_number == 1:
            print("NEAREST ", nearest_charging_station.charging_station_number)
            print("CHOOSE ", selected_charging_station.charging_station_number)

        self.charging_station_destination = selected_charging_station


