import datetime
import random

class EVQueueSimulation:
    def __init__(self, all_point, recommand_data, charge_num, charge_length, charge_pos):
        self.all_point = all_point
        self.recommand_data = recommand_data
        self.charge_num = charge_num
        self.charge_length = charge_length
        self.charge_pos = charge_pos

    def geodistance(self, lng1, lat1, lng2, lat2):
        # Calculate the geodistance between two points
        pass

    def run_simulation(self):
        wait_time_list = []
        wait_time2_list = []
        wait_num_list = []
        using_rate_list = []

        for point in self.all_point:
            wait_time_list_hour = [datetime.timedelta(hours=0)] * 12
            wait_time2_list_hour = [datetime.timedelta(hours=0)] * 12
            wait_num = 0
            wait_num2 = 0
            wait_time = datetime.timedelta(hours=0)
            wait_time2 = datetime.timedelta(hours=0)
            using_rate = 0
            charge_position = self.charge_num * [0]  # Initial 10 unoccupied charging stations

            point_data = self.recommand_data[self.recommand_data['all_point'] == point]
            point_data = point_data.sort_values('time')
            point_data_time = list(point_data['time'])
            point_data_corr = point_data.iloc[:, -2:].values

            # The rest of the simulation code from the original question goes here

        return wait_time_list, wait_time2_list, wait_num_list, using_rate_list

# Initialize the EVQueueSimulation class with appropriate parameters
simulation = EVQueueSimulation(all_point, recommand_data, charge_num, charge_length, charge_pos)
wait_time_list, wait_time2_list, wait_num_list, using_rate_list = simulation.run_simulation()
