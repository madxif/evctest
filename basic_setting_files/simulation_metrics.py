import numpy as np
import simpy


class Monitoring:
    """
    统计模拟环境运行过程中的数据
    """
    def __init__(self, ev_class, time_unit_step_size, total_simulation_time, relevant_simulation_time, number_of_charging_stations, number_of_cars, world_size):
        self.ev_class = ev_class
        self.time_unit_step_size = time_unit_step_size
        self.total_simulation_time = total_simulation_time
        self.relevant_simulation_time = relevant_simulation_time
        self.number_of_charging_stations = number_of_charging_stations
        self.number_of_cars = number_of_cars
        self.world_size = world_size
        self.resources = np.empty(self.number_of_charging_stations, dtype=simpy.Resource)
        self.repetition_counter = 0
        self.action = None
        self.cars = None
        self.charging_stations = None

        # 一些会用到的数据
        self.number_of_cars_driving = np.zeros(int(total_simulation_time / time_unit_step_size))
        self.number_of_cars_charging = np.zeros(int(total_simulation_time / time_unit_step_size))
        self.number_of_cars_waiting = np.zeros(int(total_simulation_time / time_unit_step_size))
        self.number_of_cars_on_way_to_cs = np.zeros(int(total_simulation_time / time_unit_step_size))
        self.number_of_used_spots_at_charging_stations = np.zeros(int(total_simulation_time / time_unit_step_size))
        self.waiting_time = np.zeros(int(total_simulation_time / time_unit_step_size))
        self.time_on_way_to_cs = np.zeros(int(total_simulation_time / time_unit_step_size))
        self.charging_time = np.zeros(int(total_simulation_time / time_unit_step_size))
        self.unproductive_time = np.zeros(int(total_simulation_time / time_unit_step_size))
        self.number_of_chargings = np.zeros(int(total_simulation_time / time_unit_step_size))
        self.temp_queue_size_per_cs = None
        self.temp_charge_size_per_cs = None
        self.temp_driving_to_cs_per_cs = None
        self.queue_size_per_cs = np.zeros((self.number_of_charging_stations, int(total_simulation_time / time_unit_step_size)))
        self.charge_size_per_cs = np.zeros((self.number_of_charging_stations, int(total_simulation_time / time_unit_step_size)))
        self.driving_to_cs_per_cs = np.zeros((self.number_of_charging_stations, int(total_simulation_time / time_unit_step_size)))

        # 车辆情况
        self.number_of_active_cars = None
        self.car_locations = None

    def initialize_monitoring_process(self, env, charging_stations, cars):
        """
        初始化
        """
        self.initialize_or_copy_temporary_arrays()
        self.repetition_counter += 1
        self.action = env.process(self.start_timing(env))
        self.charging_stations = charging_stations
        self.cars = cars
        for i in range(self.number_of_charging_stations):
            self.resources[i] = self.charging_stations[i].charging_spots

    def initialize_or_copy_temporary_arrays(self):
        """
        初始化绘图分析要用的数据列
        """
        if self.repetition_counter >= 1:
            self.temp_queue_size_per_cs = sorted(self.temp_queue_size_per_cs, key=sum)
            self.temp_charge_size_per_cs = sorted(self.temp_charge_size_per_cs, key=sum)
            self.temp_driving_to_cs_per_cs = sorted(self.temp_driving_to_cs_per_cs, key=sum)
            for i in range(self.number_of_charging_stations):
                self.queue_size_per_cs[i] = np.add(self.queue_size_per_cs[i], self.temp_queue_size_per_cs[i])
                self.charge_size_per_cs[i] = np.add(self.charge_size_per_cs[i], self.temp_charge_size_per_cs[i])
                self.driving_to_cs_per_cs[i] = np.add(self.driving_to_cs_per_cs[i], self.temp_driving_to_cs_per_cs[i])
        else:
            self.temp_queue_size_per_cs = np.zeros((self.number_of_charging_stations, int(self.total_simulation_time / self.time_unit_step_size)))
            self.temp_charge_size_per_cs = np.zeros((self.number_of_charging_stations, int(self.total_simulation_time / self.time_unit_step_size)))
            self.temp_driving_to_cs_per_cs = np.zeros((self.number_of_charging_stations, int(self.total_simulation_time / self.time_unit_step_size)))

    def start_timing(self, env):
        """
        按照预定义的时间间隔对数据检索过程开始计时
        """
        while True:
            self.get_information(env)
            yield env.timeout(self.time_unit_step_size)

    def get_information(self, env):
        """
        按照预定义的时间间隔统计数据
        """
        current_index = int(env.now / self.time_unit_step_size)
        if current_index >= len(self.waiting_time):
            return
        for i in range(self.number_of_charging_stations):
            self.number_of_cars_charging[current_index] += self.resources[i].count
            self.number_of_cars_waiting[current_index] += len(self.resources[i].queue)
            self.temp_queue_size_per_cs[i][current_index] = len(self.resources[i].queue)
            self.temp_charge_size_per_cs[i][current_index] = self.resources[i].count
            self.temp_driving_to_cs_per_cs[i][current_index] = len([x for x in self.cars if x.charging_station_destination == self.charging_stations[i]])
            self.number_of_cars_on_way_to_cs[current_index] += self.temp_driving_to_cs_per_cs[i][current_index]

        total_waiting_time = 0
        total_time_on_way_to_cs = 0
        total_charging_time = 0
        total_unproductive_time = 0
        total_number_of_chargings = 0
        for car in self.cars:
            #total_waiting_time += car.waiting_time
            total_time_on_way_to_cs += car.time_on_way_to_cs
            total_charging_time += car.charging_time
            total_number_of_chargings += car.number_of_chargings
        for charging_station in self.charging_stations:
            total_waiting_time += + (charging_station.get_queue_size() * self.time_unit_step_size)

        total_waiting_time += self.waiting_time[current_index - 1 if current_index > 0 else 0]
        total_unproductive_time = total_charging_time + total_waiting_time + total_time_on_way_to_cs
        self.waiting_time[current_index] = total_waiting_time
        self.time_on_way_to_cs[current_index] = total_time_on_way_to_cs
        self.charging_time[current_index] = total_charging_time
        self.unproductive_time[current_index] = total_unproductive_time
        self.number_of_chargings[current_index] = total_number_of_chargings

        self.number_of_cars_driving[current_index] = self.repetition_counter * self.number_of_cars - self.number_of_cars_charging[current_index] - self.number_of_cars_waiting[current_index]
        self.number_of_used_spots_at_charging_stations[current_index] = self.number_of_cars_charging[current_index]

    def calculate_unproductive_time(self):
        """
        统计无产出的时间及组成部分，以一次充电周期为单位划分
        """
        avg_waiting_time_by_charging_operation = np.divide(self.waiting_time, self.number_of_chargings,  out=np.zeros_like(self.waiting_time), where=self.number_of_chargings!=0)
        avg_time_to_cs_by_charging_operation = np.divide(self.time_on_way_to_cs, self.number_of_chargings,  out=np.zeros_like(self.time_on_way_to_cs), where=self.number_of_chargings!=0)
        avg_charging_time_by_charging_operation = np.divide(self.charging_time, self.number_of_chargings,  out=np.zeros_like(self.charging_time), where=self.number_of_chargings!=0)
        unproductive_time_by_charging_operation = np.divide(self.unproductive_time, self.number_of_chargings,  out=np.zeros_like(self.unproductive_time), where=self.number_of_chargings!=0)
        return unproductive_time_by_charging_operation, avg_waiting_time_by_charging_operation, avg_time_to_cs_by_charging_operation, avg_charging_time_by_charging_operation

    def calculate_cs_data(self):
        """
        统计站点的数据
        """
        combined_charging_size = self.charge_size_per_cs[0]
        combined_queue_size = self.queue_size_per_cs[0]
        combined_driving_to_cs_size = self.driving_to_cs_per_cs[0]
        for i in range(len(self.queue_size_per_cs) - 1):
            combined_charging_size = np.add(combined_charging_size, self.charge_size_per_cs[i + 1])
            combined_queue_size = np.add(combined_queue_size, self.queue_size_per_cs[i + 1])
            combined_driving_to_cs_size = np.add(combined_driving_to_cs_size, self.driving_to_cs_per_cs[i + 1])

        avg_amount_of_cars_waiting_per_charging_spot = np.zeros(len(self.charging_stations))
        avg_amount_of_cars_charging_per_charging_spot = np.zeros(len(self.charging_stations))
        for i in range(self.number_of_charging_stations):
            avg_amount_of_cars_waiting_per_charging_spot[i] = sum(self.queue_size_per_cs[i]) / (self.repetition_counter * len(self.queue_size_per_cs[i]))
            avg_amount_of_cars_charging_per_charging_spot[i] = sum(self.charge_size_per_cs[i]) / (self.repetition_counter * len(self.charge_size_per_cs[i]))

        print(combined_queue_size)
        return combined_charging_size, combined_queue_size, combined_driving_to_cs_size, avg_amount_of_cars_waiting_per_charging_spot, avg_amount_of_cars_charging_per_charging_spot

    def print_new_information(self):
        """
        输出每种策略的统计结果并保存在results中
        """
        print("每辆车的平均等待时间: {}".format(self.waiting_time[-1] / (self.number_of_cars * self.repetition_counter)))
        print("每个充电过程的平均等待时间: {}".format(self.waiting_time[-1] / self.number_of_chargings[-1]))
        print(self.waiting_time[-1])

        print("每辆车平均的寻站行驶时间: {}".format(self.time_on_way_to_cs[-1] / (self.number_of_cars * self.repetition_counter)))
        print("每个充电过程的平均寻站时间: {}".format(self.time_on_way_to_cs[-1] / self.number_of_chargings[-1]))
        print(self.time_on_way_to_cs[-1])

        print("每辆车的平均充电时间: {}".format(self.charging_time[-1] / (self.number_of_cars * self.repetition_counter)))
        print("每个充电过程的平均充电时间: {}".format(self.charging_time[-1] / self.number_of_chargings[-1]))
        print(self.charging_time[-1])

        print("每辆车平均无效时间: {}".format(self.unproductive_time[-1] / (self.number_of_cars * self.repetition_counter)))
        print("每次充电操作的平均无效时间: {}".format(self.unproductive_time[-1] / self.number_of_chargings[-1]))
        print(self.unproductive_time[-1])

        with open('results\\results.txt', 'a') as file:
            file.write("车辆名称: {} \n".format(self.ev_class.__name__))
            file.write("每次充电的平均等待时间: {} \n".format(self.waiting_time[-1] / self.number_of_chargings[-1]))
            file.write("每次充电的平均寻站行驶时间: {} \n".format(self.time_on_way_to_cs[-1] / self.number_of_chargings[-1]))
            file.write("每次充电的平均充电时间: {} \n".format(self.charging_time[-1] / self.number_of_chargings[-1]))
            file.write("每次充电的平均无效时间: {} \n \n".format(self.unproductive_time[-1] / self.number_of_chargings[-1]))


    # 车辆行为
    def save_car_data(self, env):
        """
        保存车辆的数据用于后续绘图分析
        """
        self.car_locations = np.zeros((100, 100))
        self.number_of_active_cars = np.zeros(int(self.relevant_simulation_time / self.time_unit_step_size))
        while True:
            if env.now < self.relevant_simulation_time:
                current_index = int(env.now / self.time_unit_step_size)
                for car in self.cars:
                    self.car_locations[int((car.x_coordinate/self.world_size) * 100)][int((car.y_coordinate/ self.world_size) * 100)] += 1
                if current_index < len(self.number_of_active_cars):
                    self.number_of_active_cars[current_index] = len([x for x in self.cars if x.deactivated is False])

            yield env.timeout(self.time_unit_step_size)

    def get_cs_locations_in_array(self):
        """
        保存站点的数据
        """
        charging_station_locations = np.zeros((100, 100))
        for cs in self.charging_stations:
            location = cs.get_location()
            charging_station_locations[int((location[0]/self.world_size) * 100)][int((location[1]/self.world_size) * 100)] += 1

        return charging_station_locations



