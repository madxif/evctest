from ev_implementations.ev_rcs import EVRCs
'''平均时间最短的'''

class EVRCBestByAverageTime(EVRCs):
    def __init__(self, env, world_size, x_coordinate, y_coordinate, identifying_number, charging_stations, acceptance, normal_distributed_location_data_rate,normal_charging_factor, fast_charging_factor):
        super().__init__(env, world_size, x_coordinate, y_coordinate, identifying_number, charging_stations, acceptance, normal_distributed_location_data_rate,normal_charging_factor, fast_charging_factor)
        self.track_cs = True#用于标记当前车辆是否需要追踪其充电站的使用情况
        # 对于每个充电站，计算该充电站所有可用充电桩的平均剩余充电时间，将所有充电站的平均剩余充电时间取平均值后，选择平均剩余充电时间最短的充电站作为最佳充电站。