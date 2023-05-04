import random

from ev_implementations.ev_simulation_base import BaseEV
'''
选择当前距离最近的可用快充桩的充电站
'''

class EVNearestCSWithFreeFastSpot(BaseEV):
    def set_charging_station_as_destination(self):
        selected_charging_station = None
        selected_charging_station_distance = None
        found_free_fast_spot = False
        found_free_spot = False

        # 遍历所有的充电站，计算当前电动汽车到该充电站的距离，
        # 并判断该充电站是否有可用的充电位。
        # 如果找到了一个有可用充电位的充电站，就选择它作为目标充电站。
        for charging_station in self.charging_stations:
            if self.car_number == 1:
                # 调试信息，空闲充电位和快速充电桩的数量等
                print("FFS FREE ", charging_station.charging_station_number, charging_station.get_number_of_free_spots(), charging_station.get_queue_size(), "FREE FAST ", charging_station.get_number_of_free_fast_spots())
            x, y = charging_station.get_location()
            distance = self.calculate_distance(x, y) + (abs(self.destination[0] - x) + abs(self.destination[1] - y))

            if not found_free_spot:
                if charging_station.get_number_of_free_spots() > 0:
                    selected_charging_station = charging_station
                    selected_charging_station_distance = distance
                    found_free_spot = True
                elif selected_charging_station is None or distance < selected_charging_station_distance:
                    selected_charging_station = charging_station
                    selected_charging_station_distance = distance

            # 如果当前没有找到可用充电位的充电站，那么会选择距离最近的充电站作为备选充电站。
            # 然后，查找备选充电站中是否有可用的快速充电桩。
            # 如果找到了一个有可用快速充电桩的充电站，就选作为目标充电站。
            # 如果没有找到有可用快速充电桩的充电站，就选择备选充电站中距离最近的充电站作为目标充电站。
            if found_free_spot:
                if not found_free_fast_spot:
                    if charging_station.get_number_of_free_fast_spots() > 0:
                        selected_charging_station = charging_station
                        selected_charging_station_distance = distance
                        found_free_fast_spot = True
                    elif distance < selected_charging_station_distance:
                        selected_charging_station = charging_station
                        selected_charging_station_distance = distance
                else:
                    if distance < selected_charging_station_distance and charging_station.get_number_of_free_fast_spots() > 0:
                        selected_charging_station = charging_station
                        selected_charging_station_distance = distance

        nearest_charging_station = None
        nearest_charging_station_distance = None

        for charging_station in self.charging_stations:
            nearest_x, nearest_y = charging_station.get_location()
            distance = self.calculate_distance(nearest_x, nearest_y) + (abs(self.destination[0] - nearest_x) + abs(self.destination[1] - nearest_y))
            if nearest_charging_station is None or distance < nearest_charging_station_distance:
                nearest_charging_station = charging_station
                nearest_charging_station_distance = distance

        # 检查选择的充电站是否是距离当前电动汽车最近的充电站。如果不是，那么根据
        # self.acceptance的值（取值范围为0到1），以一定概率选择距离最近的充电站作为目标充电站
        if selected_charging_station != nearest_charging_station:
            if random.randint(0,100) > self.acceptance * 100:
                selected_charging_station = nearest_charging_station

        if self.car_number == 1:
            print("NEAREST ", nearest_charging_station.charging_station_number)
            print("CHOOSE ", selected_charging_station.charging_station_number)

        self.charging_station_destination = selected_charging_station