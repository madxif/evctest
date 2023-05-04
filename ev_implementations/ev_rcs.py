from ev_implementations.ev_simulation_base import BaseEV
import random


class EVRCs(BaseEV):
    def __init__(self, env, world_size, x_coordinate, y_coordinate, identifying_number, charging_stations, acceptance, normal_distributed_location_data_rate, normal_charging_factor, fast_charging_factor):
        super().__init__(env, world_size, x_coordinate, y_coordinate, identifying_number, charging_stations, acceptance, normal_distributed_location_data_rate, normal_charging_factor, fast_charging_factor)
        self.rc = None # 推荐系统
        self.nearest = False # 是否使用最近站点
        self.track_cs = False # 是否跟踪充电站

    def get_recommendation_center(self, rc):
        """
        设置推荐系统
        """
        self.rc = rc

    def set_charging_station_as_destination(self):
        """
        将推荐系统推荐的站点作为目标站点
        """
        selected_charging_station = self.rc.recommend_charging_station(self)
        self.charging_station_destination = selected_charging_station

    def run(self):
        """
        模拟环境中的主要运行过程,处理车辆的行为
        """
        while True:
            if not self.deactivated:
                self.generate_random_destination() # 随机生成目的地
                self.set_charging_station_as_destination() # 将推荐站点设置为目标站点

                # 计算到达推荐站点需要的时间
                direct_distance = self.calculate_distance(self.destination[0], self.destination[1])
                time_on_way_to_cs = self.calculate_distance(self.charging_station_destination.get_location()[0], self.charging_station_destination.get_location()[1]) + \
                                          (abs(self.destination[0] - self.charging_station_destination.get_location()[0]) + abs(self.destination[1] - self.charging_station_destination.get_location()[1])) - direct_distance

                self.time_on_way_to_cs += time_on_way_to_cs# 更新到站点的时间
                if self.car_number == 1:
                    print("DRIVING: ", self.env.now)# 打印状态
                self.number_of_chargings += 1# 增加充电次数

                yield self.drive_to_location() # 行驶到目的地

                #充电
                charging_spot = self.charging_station_destination.allocate_charging_spot() # 获取充电站的充电位
                cs = self.charging_station_destination# 获取充电站
                self.charging_station_destination = None
                #print("test", self.destination, self.x_coordinate, self.y_coordinate)
                if self.car_number == 1:
                    print("WAITING: ", self.env.now)# 打印状态

                # 等待充电位
                waiting_start = self.env.now
                with charging_spot.request() as req:
                    yield req

                    waiting_end = self.env.now

                    waiting_time = waiting_end - waiting_start# 计算等待时间
                    if self.track_cs:
                        self.rc.add_waiting_time_to_cs(cs.charging_station_number, waiting_time)

                    #print(self.charging_station_destination)

                    if self.car_number == 1:#前面没有其他车辆
                        print("CHARGING: ", self.env.now)# 打印状态
                    is_fast_charging_spot = cs.check_free_fast_spot()# 检查是否有快速充电位

                    # 计算快速充电需要的时间，更新车辆离开充电站的时间
                    if is_fast_charging_spot:
                        charging_time = int((1000000 - self.energy_units) * self.fast_charging_factor)#车辆的能量单元设置为1000000
                        leaving_time = self.env.now + int((1000000 - self.energy_units) * self.fast_charging_factor)
                        self.rc.future_cs_departures[cs.charging_station_number].append(leaving_time)
                        self.rc.future_fast_spots_departures[cs.charging_station_number].append(leaving_time)
                    else:
                        # 计算普通充电需要的时间，更新车辆离开的时间
                        leaving_time = self.env.now + int((1000000 - self.energy_units) * self.normal_charging_factor)
                        self.rc.future_cs_departures[cs.charging_station_number].append(leaving_time)
                        charging_time = int((1000000 - self.energy_units) * self.normal_charging_factor)
                    self.charging_time += charging_time
                    if self.track_cs:#记录站点的数据
                        self.rc.add_charging_time_to_cs(cs.charging_station_number, charging_time)
                        self.rc.add_charging_to_cs(cs.charging_station_number)

                    yield self.start_charging(is_fast_charging_spot)#表示车辆正在进行充电，直到充电完成
                    if is_fast_charging_spot:
                        cs.free_up_fast_spot()#如果车辆正在快速充电位上，则将其标记为已释放快速充电位

                    #print("yo", self.env.now, car_index, self.car_number, self.rc.cars_arriving_list[cs.charging_station_number][car_index],self.rc.future_cs_arrivals[cs.charging_station_number][car_index])

                    # 如果车辆不必须选择最近的充电站，则在充电完成后从相关列表中删除车辆的信息
                    if not self.nearest:
                        car_index = self.rc.cars_arriving_list[cs.charging_station_number].index(self.car_number)
                        departure_index = self.rc.future_cs_departures[cs.charging_station_number].index(leaving_time)

                        del self.rc.cars_arriving_list[cs.charging_station_number][car_index]
                        del self.rc.future_cs_arrivals[cs.charging_station_number][car_index]
                        del self.rc.future_cs_departures[cs.charging_station_number][departure_index]
                        if is_fast_charging_spot:#如果车辆正在快速充电位上，清除相关信息
                            if self.car_number in self.rc.cars_arriving_fast_spots_list[cs.charging_station_number]:
                                fast_spot_car_index = self.rc.cars_arriving_fast_spots_list[cs.charging_station_number].index(self.car_number)
                                fast_spot_departure_index = self.rc.future_fast_spots_departures[cs.charging_station_number].index(leaving_time)
                                del self.rc.cars_arriving_fast_spots_list[cs.charging_station_number][fast_spot_car_index]
                                del self.rc.future_fast_spots_arrivals[cs.charging_station_number][fast_spot_car_index]
                                del self.rc.future_fast_spots_departures[cs.charging_station_number][fast_spot_departure_index]

                    self.energy_units = 1000000 #将车辆的能量单元设置为1000000


                # 结束充电
                if self.car_number == 1:
                    print("DONE: ", self.env.now)
                if self.car_number == 1:
                    print("FAST: ", is_fast_charging_spot)

                # 行驶到新的随机位置
                yield self.drive_to_location()
                trip_duration = random.randint(10000, 20000)
                # 计算并减少车辆的能量单元，以模拟车辆在行驶过程中的能量消耗
                self.energy_units = self.energy_units - trip_duration
                # 告诉模拟器，当前车辆需要运行 trip_duration 的时间才能进行下一段任务
                # 等待时间结束后模拟器会恢复当前协程的执行
                # 在等待期间，模拟环境会让其他协程继续执行，即其他车辆仍保持运行
                # 等待结束后，再执行下一行
                yield self.env.timeout(trip_duration)

                if self.car_number == 1:
                    print("AT_RAND_LOCATION: ", self.env.now)
            else:
                # 若标记为下线状态，执行park()
                yield self.park()

