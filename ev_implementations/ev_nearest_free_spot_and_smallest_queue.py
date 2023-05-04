import random

from ev_implementations.ev_simulation_base import BaseEV
'''选择最近的空闲的或者最短排队的'''

class EVCombined(BaseEV):
    def set_charging_station_as_destination(self):
        selected_charging_station = None
        selected_charging_station_distance = None
        selected_charging_station_queue_size = None
        found_free_spot = False

        # 遍历所有可用的充电站，找到最近的充电站，并检查它是否有可用的充电空间
        # 如果有可用的空间，选择该充电站作为目的地，并记录该充电站的距离和队列大小
        # 如果没有可用的空间，则检查该充电站的队列大小是否比已选择的充电站更小
        # 如果是，选择该充电站。如果队列大小相同，则选择最近的充电站
        for charging_station in self.charging_stations:
            if self.car_number == 1:
                print("HYBRID FREE ", charging_station.charging_station_number, charging_station.get_number_of_free_spots(), charging_station.get_queue_size())
            x, y = charging_station.get_location()
            distance = self.calculate_distance(x, y) + (abs(self.destination[0] - x) + abs(self.destination[1] - y))
            if not found_free_spot:
                if charging_station.get_number_of_free_spots() > 0:
                    selected_charging_station = charging_station
                    selected_charging_station_distance = distance
                    selected_charging_station_queue_size = selected_charging_station.get_queue_size()
                    found_free_spot = True
                elif selected_charging_station_queue_size is not None and charging_station.get_queue_size() < selected_charging_station_queue_size:
                    selected_charging_station = charging_station
                    selected_charging_station_distance = distance
                    selected_charging_station_queue_size = selected_charging_station.get_queue_size()
                elif selected_charging_station is None or (charging_station.get_queue_size() == selected_charging_station_queue_size and distance < selected_charging_station_distance):
                    selected_charging_station = charging_station
                    selected_charging_station_distance = distance
                    selected_charging_station_queue_size = selected_charging_station.get_queue_size()
            else:
                if distance < selected_charging_station_distance and charging_station.get_number_of_free_spots() > 0:
                    selected_charging_station = charging_station
                    selected_charging_station_distance = distance

        nearest_charging_station = None
        nearest_charging_station_distance = None

        # 如果已经找到了可用的充电站，检查是否有更近的空闲充电站，并选择最近的空闲充电站作为目的地
        for charging_station in self.charging_stations:
            nearest_x, nearest_y = charging_station.get_location()
            distance = self.calculate_distance(nearest_x, nearest_y) + (abs(self.destination[0] - nearest_x) + abs(self.destination[1] - nearest_y))
            if nearest_charging_station is None or distance < nearest_charging_station_distance:
                nearest_charging_station = charging_station
                nearest_charging_station_distance = distance

        # 如果选择的充电站不是最近的充电站，并且随机数大于指定的接受度，则选择最近的充电站
        if selected_charging_station != nearest_charging_station:
            if random.randint(0, 100) > self.acceptance * 100:
                selected_charging_station = nearest_charging_station

        if self.car_number == 1:
            print("NEAREST ", nearest_charging_station.charging_station_number)
            print("CHOOSE ", selected_charging_station.charging_station_number)

        self.charging_station_destination = selected_charging_station