from ev_implementations.ev_rcs import EVRCs
'''
用时最短的
'''

class EVRCSmallestAmountOfTimeLost(EVRCs):
    def __init__(self, env, world_size, x_coordinate, y_coordinate, identifying_number, charging_stations, acceptance, normal_distributed_location_data_rate, normal_charging_factor, fast_charging_factor):
        super().__init__(env, world_size, x_coordinate, y_coordinate, identifying_number, charging_stations, acceptance, normal_distributed_location_data_rate, normal_charging_factor, fast_charging_factor)
        