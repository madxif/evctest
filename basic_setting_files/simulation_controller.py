from .simulation_parameters import TIME_FACTOR, ENV_ENTIRE_LENGTH
import numpy as np

'''
控制仿真过程中的时间因素
'''

class SimulationController:
    def __init__(self, env, cars, charging_stations):
        self.env = env
        self.cars = cars
        self.charging_stations = charging_stations
        self.action = env.process(self.control_time_factor())

    def control_time_factor(self):#每次循环中计算当前时间的小时数
        while True:
            if (self.env.now / 60) % 60 == 0:
                time_factor_current = TIME_FACTOR[((self.env.now/60)/60) % 24]#从 TIME_FACTOR 列表中获取当前时间因素
                cars_needed = np.random.normal(time_factor_current * len(self.cars), len(self.cars) / 50)#计算需要多少辆车来满足这个时间因素
                for car in self.cars:#遍历所有的车辆，并检查它们是否应该继续行驶或被停用
                    if self.env.now <= ENV_ENTIRE_LENGTH:#如果当前时间已经超过了仿真的整个长度，那么停用车辆
                        if car.car_number > cars_needed:
                            car.deactivated = True
                        else:
                            car.continue_driving()
                    else:
                        car.deactivated = True
            yield self.env.timeout(100)





