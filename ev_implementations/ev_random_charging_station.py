from ev_implementations.ev_simulation_base import BaseEV
import random
'''
随机选取充电站，必要时将其替换为距离目的地更近的充电站
'''

class EVRandomCS(BaseEV):
    def set_charging_station_as_destination(self):
        # 从可用充电站列表中随机选择一个充电站，作为电动汽车的目的地充电站
        selected_charging_station = random.choice(self.charging_stations)

        nearest_charging_station = None
        nearest_charging_station_distance = None

        # 查找距离目的地最近的充电站，如果随机数超过指定的acceptance值，则将目的地充电站设置为最近的充电站
        for charging_station in self.charging_stations:
            nearest_x, nearest_y = charging_station.get_location()
            distance = self.calculate_distance(nearest_x, nearest_y) + (abs(self.destination[0] - nearest_x) + abs(self.destination[1] - nearest_y))
            if nearest_charging_station is None or distance < nearest_charging_station_distance:
                nearest_charging_station = charging_station
                nearest_charging_station_distance = distance

        if selected_charging_station != nearest_charging_station:
            if random.randint(0, 100) > self.acceptance * 100:
                selected_charging_station = nearest_charging_station

        self.charging_station_destination = selected_charging_station
