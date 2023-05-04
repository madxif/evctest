import random

from ev_implementations.ev_simulation_base import BaseEV


class EVNearestCSWithFreeChargingSpot(BaseEV):
    def set_charging_station_as_destination(self):
        selected_charging_station = None
        selected_charging_station_distance = None
        found_free_spot = False

        # 循环检查所有充电站，并找到距离车辆最近的充电站
        for charging_station in self.charging_stations:
            if self.car_number == 1:
                print("F FREE ", charging_station.charging_station_number, charging_station.get_number_of_free_spots(), charging_station.get_queue_size())
            x, y = charging_station.get_location()
            # 计算站点的距离
            distance = self.calculate_distance(x, y) + (abs(self.destination[0] - x) + abs(self.destination[1] - y))
            if not found_free_spot:#检查该充电站是否有可用充电桩
                if charging_station.get_number_of_free_spots() > 0:
                    selected_charging_station = charging_station
                    selected_charging_station_distance = distance
                    found_free_spot = True
                elif selected_charging_station is None or distance < selected_charging_station_distance:
                    selected_charging_station = charging_station
                    selected_charging_station_distance = distance
            else:# 如果没有，则比较当前最佳充电站（如果已有）和新充电站的距离，并选择最近的充电站
                if distance < selected_charging_station_distance and charging_station.get_number_of_free_spots() > 0:
                    selected_charging_station = charging_station
                    selected_charging_station_distance = distance

        nearest_charging_station = None
        nearest_charging_station_distance = None

        # 如果有多个充电站的距离相同，则选择最近可用站点
        for charging_station in self.charging_stations:
            nearest_x, nearest_y = charging_station.get_location()
            distance = self.calculate_distance(nearest_x, nearest_y) + (abs(self.destination[0] - nearest_x) + abs(self.destination[1] - nearest_y))
            if nearest_charging_station is None or distance < nearest_charging_station_distance:
                nearest_charging_station = charging_station
                nearest_charging_station_distance = distance

        if selected_charging_station != nearest_charging_station:#比较选择的充电站和最近的充电站是否相同，如果不同，则以一定的概率接受最近的充电站作为目的地
            if random.randint(0,100) > self.acceptance * 100:#介于0到1之间的参数，用于控制接受最近充电站的概率
                selected_charging_station = nearest_charging_station

        if self.car_number == 1:
            print("NEAREST ", nearest_charging_station.charging_station_number)
            print("CHOOSE ", selected_charging_station.charging_station_number)

        self.charging_station_destination = selected_charging_station
