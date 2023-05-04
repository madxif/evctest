from ev_implementations.ev_no_charge import EVNoCharge
from ev_implementations.ev_simulation_nearest_cs import EVNearestCS
from ev_implementations.ev_least_frequented_cs import EVLeastFrequented
from ev_implementations.ev_nearest_free_spot_and_smallest_queue import EVCombined
from ev_implementations.ev_rc_equal_distribution import EVRCEqualDistribution
from ev_implementations.ev_random_charging_station import EVRandomCS
from ev_implementations.ev_nearest_with_free_fast_spot import EVNearestCSWithFreeFastSpot
from ev_implementations.ev_rc_best_by_average_time import EVRCBestByAverageTime
from cs_implementatons.cs_simulation_base import ChargingStation
from rc_implementations.rc_best_by_average_time_tracking import RCBestByAverageTime
from rc_implementations.rc_equal_distribution import RCEqualDistribution
from basic_setting_files.plotting import plot_line_graph, plot_bar_graph, plot_heatmap
from basic_setting_files.generating_methods import generate_charging_station_locations, run_simulation, run_simulation_with_rc, run_simulate_car_behaviour, run_simulation_parameters, run_simulation_rc_parameters, generate_charging_station_locations_parameters
from basic_setting_files.simulation_parameters import LENGTH_OF_SIMULATION, NUMBER_OF_TOTAL_CARS, num_stations, world_size,\
    NUMBER_OF_REPETITIONS, station_capacity, INFORMATION_TIME_UNIT_STEP_SIZE, ADVICE_FOLLOW_RATE_FOR_NON_NEAREST_CS, \
    NORMAL_DISTRIBUTED_DATA_RATE, NUMBER_OF_FAST_CHARGERS, NORMAL_CHARGING_FACTOR, FAST_CHARGING_FACTOR, ENV_ENTIRE_LENGTH
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['simhei']###解决绘图显示中文乱码
plt.rcParams['axes.unicode_minus']=False

import numpy as np

def main():
    # 读取地图新划定范围
    shapefile_path = 'mapdata/SZ_Landuse_Simplified.shp'
    # map_data = read_shapefile(shapefile_path)
    # print(map_data)
    # print(type(map_data))

    # 生成充电站的位置
    charging_station_locations = generate_charging_station_locations(world_size, num_stations, shapefile_path, station_capacity)
    print(charging_station_locations)

    choice = input("1: 只展示车辆行为 \n"
                   "2: 对比分析 \n")
    # Show car behaviour
    if choice == '1':
        show_car_behaviour(charging_station_locations)

    elif choice == '2':
        with open('results\\results.txt', 'w',encoding="UTF-8") as file:
            file.write("Results: \n")
            file.write("world_size = {} \n".format(world_size))
            file.write("num_stations = {} \n".format(num_stations))
            file.write("NUMBER_OF_TOTAL_CARS = {} \n".format(NUMBER_OF_TOTAL_CARS))
            file.write("LENGTH_OF_SIMULATION = {} \n".format(LENGTH_OF_SIMULATION))
            file.write("ACTIVE LENGTH = {} \n".format(ENV_ENTIRE_LENGTH))
            file.write("NUMBER_OF_REPETITIONS = {} \n".format(NUMBER_OF_REPETITIONS))
            file.write("station_capacity = {} \n".format(station_capacity))
            file.write("INFORMATION_TIME_UNIT_STEP_SIZE = {} \n".format(INFORMATION_TIME_UNIT_STEP_SIZE))
            file.write("ADVICE_FOLLOW_RATE_FOR_NON_NEAREST_CS = {} \n".format(ADVICE_FOLLOW_RATE_FOR_NON_NEAREST_CS))
            file.write("NORMAL_DISTRIBUTED_DATA_RATE = {} \n".format(NORMAL_DISTRIBUTED_DATA_RATE))
            file.write("NUMBER_OF_FAST_CHARGERS = {} \n".format(NUMBER_OF_FAST_CHARGERS))
            file.write("NORMAL_CHARGING_FACTOR = {} \n".format(NORMAL_CHARGING_FACTOR))
            file.write("FAST_CHARGING_FACTOR = {} \n \n".format(FAST_CHARGING_FACTOR))

        show_car_behaviour(charging_station_locations)

        # 司机只能前往充电站获取当前在充电的和排队中的车辆情况，充电站只知道自己站点的情况
        monitoringEVRandomCS = run_simulation(EVRandomCS, ChargingStation, charging_station_locations)
        monitoringEVRandomCS.print_new_information()
        monitoringEVNearestCS = run_simulation(EVNearestCS, ChargingStation, charging_station_locations)
        monitoringEVNearestCS.print_new_information()
        monitoringEVLeastFrequented = run_simulation(EVLeastFrequented, ChargingStation, charging_station_locations)
        monitoringEVLeastFrequented.print_new_information()
        monitoringEVNearestCSWithFreeFastSpot = run_simulation(EVNearestCSWithFreeFastSpot, ChargingStation, charging_station_locations)
        monitoringEVNearestCSWithFreeFastSpot.print_new_information()
        monitoringEVCombined = run_simulation(EVCombined, ChargingStation, charging_station_locations)
        monitoringEVCombined.print_new_information()

        # 系统服务器知道每个司机的位置和他们的目标充电站，以及每个站点正在充电的和排队的车辆
        monitoringEVRCBestByAverageTime = run_simulation_with_rc(EVRCBestByAverageTime, ChargingStation, RCBestByAverageTime, charging_station_locations)
        monitoringEVRCBestByAverageTime.print_new_information()
        monitoringEVRCEqualDistribution = run_simulation_with_rc(EVRCEqualDistribution, ChargingStation, RCEqualDistribution, charging_station_locations)
        monitoringEVRCEqualDistribution.print_new_information()

        compare_simulations([monitoringEVRandomCS, monitoringEVNearestCS, monitoringEVNearestCSWithFreeFastSpot, monitoringEVLeastFrequented, monitoringEVCombined, monitoringEVRCBestByAverageTime, monitoringEVRCEqualDistribution])

    elif choice == "3":
        test_performances()


def show_car_behaviour(charging_station_locations):
    """
    展示车辆的行为以及车辆及充电站的位置.
    同时展示不同时间电动车不同分布的效果
    """
    monitoringEVNoCharge = run_simulate_car_behaviour(EVNoCharge, ChargingStation, charging_station_locations)
    plot_heatmap(monitoringEVNoCharge.car_locations, "电动车位置分布情况")
    plot_heatmap(monitoringEVNoCharge.get_cs_locations_in_array(), "充电站分布位置")
    x = np.arange(0, len(monitoringEVNoCharge.number_of_active_cars))
    plot_line_graph(x, [monitoringEVNoCharge.number_of_active_cars], "城市中活跃的车辆数", None, "时间", "活跃的车辆数", 0, 240, 0, NUMBER_OF_TOTAL_CARS)


def compare_simulations(monitoring_list):
    """
    对比不同情况的模拟结果.
    """

    # 绘制等待时间, 驾驶时间, 充电时间以及无效的时间
    x = np.arange(0, LENGTH_OF_SIMULATION if LENGTH_OF_SIMULATION % INFORMATION_TIME_UNIT_STEP_SIZE == 0 else LENGTH_OF_SIMULATION - INFORMATION_TIME_UNIT_STEP_SIZE, INFORMATION_TIME_UNIT_STEP_SIZE)
    unproductive_time_all = []
    avg_waiting_time_all = []
    avg_time_to_cs_all = []
    avg_charging_time_all = []
    labels = []
    for i in range(len(monitoring_list)):
        unproductive_time_by_charging_operation, avg_waiting_time_by_charging_operation, avg_time_to_cs_by_charging_operation, avg_charging_time_by_charging_operation = monitoring_list[i].calculate_unproductive_time()
        unproductive_time_all.append(unproductive_time_by_charging_operation)
        avg_waiting_time_all.append(avg_waiting_time_by_charging_operation)
        avg_time_to_cs_all.append(avg_time_to_cs_by_charging_operation)
        avg_charging_time_all.append(avg_charging_time_by_charging_operation)
        labels.append(monitoring_list[i].ev_class.__name__)

    plot_line_graph(x, avg_waiting_time_all, "平均每次充电的等待时间", labels, "时间", "充电等待时间")
    plot_line_graph(x, avg_time_to_cs_all, "平均每次充电行驶的时间", labels, "时间", "寻站行驶时间")
    plot_line_graph(x, avg_charging_time_all, "平均每次充电花费的总时间", labels, "时间", "充电花费时间")
    plot_line_graph(x, unproductive_time_all, "平均每次充电无效的时间", labels, "时间", "每次充电的无效时间")

    # NOT USED
    #combined_charging_all = []
    #combined_queue_all = []
    #combined_driving_all = []
    #for i in range(len(monitoring_list)):
    #    combined_charging_size, combined_queue_size, combined_driving_to_cs_size, _, __ = monitoring_list[i].calculate_cs_data()
    #    combined_charging_all.append(np.divide(combined_charging_size, (num_stations * station_capacity * NUMBER_OF_REPETITIONS)))
    #    combined_queue_all.append(np.divide(combined_queue_size, (num_stations * station_capacity * NUMBER_OF_REPETITIONS)))
    #    combined_driving_all.append(np.divide(combined_driving_to_cs_size, (num_stations * station_capacity * NUMBER_OF_REPETITIONS)))

    #plot_nice_line_graph(x, combined_charging_all, "Amount of cars charging per charging spot", labels, "Time", "Cars charging per charging spot", 0, 173000, 0, 1)

    #plot_nice_line_graph(x, combined_queue_all, "Amount of cars waiting per charging spot", labels, "Time", "Cars waiting per charging spot")

    #plot_nice_line_graph(x, combined_driving_all, "Amount of cars driving to CS per charging spot", labels, "Time", "Cars driving to CS per charging spot")

    # Plots average amount of cars per CS
    x = np.arange(0, num_stations)
    avg_amount_of_cars_waiting_per_charging_spot_all = []
    avg_amount_of_cars_charging_per_charging_spot_all = []

    for i in range(len(monitoring_list)):
        _, __, ___, avg_amount_of_cars_waiting_per_charging_spot, avg_amount_of_cars_charging_per_charging_spot = monitoring_list[i].calculate_cs_data()
        avg_amount_of_cars_waiting_per_charging_spot_all.append(avg_amount_of_cars_waiting_per_charging_spot)
        avg_amount_of_cars_charging_per_charging_spot_all.append(avg_amount_of_cars_charging_per_charging_spot)
        max_y = 0
        max_y = max(max_y, max(avg_amount_of_cars_waiting_per_charging_spot) + 10)

    # for i in range(len(monitoring_list)):
        plot_bar_graph(x, avg_amount_of_cars_charging_per_charging_spot_all[i], avg_amount_of_cars_waiting_per_charging_spot_all[i],
                            "每个站点充电的车辆 ({})".format(monitoring_list[i].ev_class.__name__), "充电站编号", "平均充电车辆数", 0, max_y)
#
# NOT USED HERE
#
def test_performances():
    # parameter_list_to_change = [5, 10, 20, 50, 100]
    parameter_list_to_change = [0.01, 0.02, 0.1, 0.2, 0.4, 1, 2, 6, 10]
    results = []
    for i in range(4):
         results.append(np.zeros(len(parameter_list_to_change)))

    result_counter = 0
    for parameter in parameter_list_to_change:
        charging_station_locations = generate_charging_station_locations_parameters(parameter)
        print("Parameter run ", result_counter + 1)
        number_of_cs = parameter
        number_of_total_cars = NUMBER_OF_TOTAL_CARS
        normal_charging_factor = NORMAL_CHARGING_FACTOR
        fast_charging_factor = FAST_CHARGING_FACTOR
        capacity_per_cs = station_capacity

        monitoringEVRandomCS = run_simulation_parameters(EVRandomCS, ChargingStation, charging_station_locations, number_of_total_cars, number_of_cs, normal_charging_factor, fast_charging_factor, capacity_per_cs)
        monitoringEVNearestCS = run_simulation_parameters(EVNearestCS, ChargingStation, charging_station_locations, number_of_total_cars, number_of_cs, normal_charging_factor, fast_charging_factor, capacity_per_cs)
        monitoringEVNearestCSWithFreeFastSpot = run_simulation_parameters(EVNearestCSWithFreeFastSpot, ChargingStation, charging_station_locations, number_of_total_cars, number_of_cs, normal_charging_factor, fast_charging_factor, capacity_per_cs)
        monitoringEVNearestCSWithFreeCSAndSmallestQueue = run_simulation_parameters(EVLeastFrequented, ChargingStation, charging_station_locations, number_of_total_cars, number_of_cs, normal_charging_factor, fast_charging_factor, capacity_per_cs)


        results[0][result_counter] = monitoringEVRandomCS.unproductive_time[-1] / monitoringEVRandomCS.number_of_chargings[-1]
        results[1][result_counter] = monitoringEVNearestCS.unproductive_time[-1] / monitoringEVNearestCS.number_of_chargings[-1]
        results[2][result_counter] = monitoringEVNearestCSWithFreeFastSpot.unproductive_time[-1] /monitoringEVNearestCSWithFreeFastSpot.number_of_chargings[-1]
        results[3][result_counter] = monitoringEVNearestCSWithFreeCSAndSmallestQueue.unproductive_time[-1] / monitoringEVNearestCSWithFreeCSAndSmallestQueue.number_of_chargings[-1]
        result_counter += 1

    name_list = ["随机", "最近的", "有空闲快充桩的CS", "最少有人去的CS" ]# "最小时间损耗", "均匀分布"]

    for n in range(len(name_list)):
        plt.plot(parameter_list_to_change, results[n], label=str(name_list[n]))
    plt.title("无产出时间对比")
    plt.legend(loc="upper left")
    plt.show()



if __name__ == "__main__":
    main()
