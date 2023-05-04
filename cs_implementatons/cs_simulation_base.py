import simpy
from basic_setting_files.simulation_parameters import NUMBER_OF_FAST_CHARGERS


class ChargingStation(object):
    def __init__(self, env, x_coordinate, y_coordinate, identifying_number, car_capacity):
        self.env = env
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.charging_station_number = identifying_number
        self.car_capacity = car_capacity
        self.charging_spots = simpy.Resource(env, capacity=self.car_capacity)
        self.fast_charging_places = int(self.car_capacity * NUMBER_OF_FAST_CHARGERS)

    def get_location(self):
        """
        返回该站点的位置
        """
        return self.x_coordinate, self.y_coordinate

    def allocate_charging_spot(self):
        """
        返回给请求充电的车辆一个桩或者将其添加到队列里面
        """
        return self.charging_spots

    def check_free_fast_spot(self):
        """
        如果有可用的快充桩就返回True
        """
        if self.fast_charging_places > 0:
            self.fast_charging_places -= 1
            return True
        else:
            return False

    def free_up_fast_spot(self):
        """
        表示快充桩分配完了
        """
        self.fast_charging_places += 1

    def get_number_of_free_spots(self):
        """
        返回空闲充电桩的数量
        """
        return self.charging_spots.capacity - self.charging_spots.count

    def get_number_of_free_fast_spots(self):
        """
        返回空闲快充桩的数量
        """
        return self.fast_charging_places

    def get_queue_size(self):
        """
        返回排队的车辆数目
        """
        return len(self.charging_spots.queue)

    def get_number_of_cars(self):
        """
        返回当前站点车辆总数，包括在充电的和等待充电的
        """
        return self.charging_spots.count + len(self.charging_spots.queue)
