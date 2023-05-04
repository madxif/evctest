from ev_implementations.ev_simulation_base import BaseEV
'''
直接去最近的充电站，不考虑站点使用情况或者排队情况
遍历了所有充电站，计算出到每个充电站的距离，并选择距离最近的充电站作为目的地。
如果有多个距离相等的充电站，随机选择一个
'''

class EVNearestCS(BaseEV):
    def set_charging_station_as_destination(self):
        selected_charging_station = None
        selected_charging_station_distance = None

        for charging_station in self.charging_stations:
            if self.car_number == 1:
                print("NEAREST FREE ", charging_station.charging_station_number, charging_station.get_number_of_free_spots(), charging_station.get_queue_size())
            x, y = charging_station.get_location()
            distance = self.calculate_distance(x, y) + (abs(self.destination[0] - x) + abs(self.destination[1] - y))
            if selected_charging_station is None or distance < selected_charging_station_distance:
                selected_charging_station = charging_station
                selected_charging_station_distance = distance

        if self.car_number == 1:
            print("CHOOSE ", selected_charging_station.charging_station_number)



        self.charging_station_destination = selected_charging_station #返回选择的充电站作为目的地




