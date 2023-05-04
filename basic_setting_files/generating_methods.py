import random
from basic_setting_files.simulation_parameters import LENGTH_OF_SIMULATION, NUMBER_OF_TOTAL_CARS, num_stations, world_size, \
    NUMBER_OF_REPETITIONS, station_capacity, INFORMATION_TIME_UNIT_STEP_SIZE, ADVICE_FOLLOW_RATE_FOR_NON_NEAREST_CS, \
    NORMAL_DISTRIBUTED_DATA_RATE, NUMBER_OF_FAST_CHARGERS, NORMAL_CHARGING_FACTOR, FAST_CHARGING_FACTOR, \
    ENV_ENTIRE_LENGTH
from basic_setting_files.simulation_metrics import Monitoring
from basic_setting_files.simulation_controller import SimulationController
import simpy
import numpy as np
# import random
# import shapefile
#
# import geopandas as gpd
# import rasterio.features
# from rasterio.transform import from_bounds

# def read_shapefile(filename='shenzhen.shp', resolution=100):
#     # 读取shp文件
#     data = gpd.read_file(filename)
#     # 将地图转换为栅格
#     bounds = data.total_bounds
#     transform = from_bounds(*bounds, resolution, resolution)
#     out_shape = (int((bounds[3]-bounds[1])/resolution), int((bounds[2]-bounds[0])/resolution))
#     raster = rasterio.features.rasterize(shapes=data.geometry, out_shape=out_shape, transform=transform)
#     # 将不需要的区域置为0
#     raster[raster != 0] = 1
#     return raster

import geopandas as gpd
import random

# def read_shapefile(filename):
#     gdf = gpd.read_file(filename)
#     return gdf.geometry.unary_union.bounds
#
# def generate_charging_station_locations(filename, num_stations, world_size):
#     bounds = read_shapefile(filename)
#     x_min, y_min, x_max, y_max = bounds
#
#     #算出每个小格的尺寸
#     grid_size = (x_max - x_min) / world_size
#
#     # 构建一个覆盖完整地图的网格世界
#     cells = []
#     for i in range(world_size):
#         for j in range(world_size):
#             cell_x_min = x_min + i * grid_size
#             cell_y_min = y_min + j * grid_size
#             cell_x_max = cell_x_min + grid_size
#             cell_y_max = cell_y_min + grid_size
#             cells.append((cell_x_min, cell_y_min, cell_x_max, cell_y_max))
#
#     # 加载地图信息去掉多余部分
#     gdf = gpd.read_file(filename)
#     gdf = gdf[gdf.geometry.within(bounds)]
#
#     # 从过滤后的格子中随机选取作为站点位置Randomly select points from the filtered shapefile to be charging stations
#     stations = random.sample(list(gdf.geometry), num_stations)
#
#     # Assign each station to a grid cell
#     assigned_cells = {}
#     for station in stations:
#         for i, cell in enumerate(cells):
#             if station.x >= cell[0] and station.x < cell[2] and station.y >= cell[1] and station.y < cell[3]:
#                 if i in assigned_cells:
#                     assigned_cells[i].append(station)
#                 else:
#                     assigned_cells[i] = [station]
#
#     # 计算每个栅格的中心点
#     center_points = [(cell[0] + cell[2]) / 2, (cell[1] + cell[3]) / 2] for cell in cells]
#
#     # 找到栅格中心点最近的充电站
#     # Find the closest charging station to each center point
#     closest_stations = []
#     for center_point in center_points:
#         closest_station = None
#         closest_distance = float('inf')
#         for station in assigned_cells[0]:
#             distance = ((station.x - center_point[0])**2 + (station.y - center_point[1])**2)**0.5
#             if distance < closest_distance:
#                 closest_station = station
#                 closest_distance = distance
#         closest_stations.append(closest_station)
#
#     # Return the coordinates of the closest charging station to each grid cell
#     return [(station.x, station.y) for station in closest_stations]


# import random
# from typing import List, Tuple
# from shapely.geometry import Polygon, Point, box
# import geopandas as gpd
#
#
# def generate_charging_station_locations(world_size: int, num_stations: int,
#                                         map_file: str, station_capacity: int) -> List[Tuple[float, float, int]]:
#     """
#     读取shp地图数据，并栅格化，对照以world_size为边长的矩形世界，生成num_stations个充电站的位置坐标和容量信息，
#     并返回站点坐标的列表。
#
#     参数：
#     world_size: int，矩形世界的边长。
#     num_stations: int，生成的充电站数量。
#     map_file: str，shp地图数据文件路径。
#     station_capacity: int，每个充电站的容量，也就是有多少充电桩。
#
#     返回：
#     # List[Tuple[float, float, int]]，包含num_stations个充电站位置坐标和容量信息的列表，每个元素为一个包含3个值的元组，分别为
#     # 充电站所在位置的x坐标、y坐标和容量。
#
#     返回多轮生成的结果列表
#     """
#     # 读取shp地图数据
#     gdf = gpd.read_file(map_file)#GeoDataFrame
#     # 将地图数据转换为多边形列表
#     polygons = list(gdf.geometry)
#
#     # 将地图数据栅格化
#     # 计算栅格的边长(total_bounds返回的是一个(minx,miny,maxx,maxy)的值
#     # 为了能够完全覆盖整个地图，这里以最长的边为基准来计算单个网格的大小，以确保网格足够细致
#     grid_size = max(gdf.total_bounds[2] - gdf.total_bounds[0], gdf.total_bounds[3] - gdf.total_bounds[1]) / world_size
#     # 计算栅格的行数和列数
#     rows = int(max(gdf.total_bounds[2] - gdf.total_bounds[0], gdf.total_bounds[3] - gdf.total_bounds[1]) / grid_size)
#     cols = int(min(gdf.total_bounds[2] - gdf.total_bounds[0], gdf.total_bounds[3] - gdf.total_bounds[1]) / grid_size)
#
#     # 生成充电站位置信息
#     charging_station_locations = []
#
#     for i in range(NUMBER_OF_REPETITIONS):
#         location_per_run = []
#         # 创建一个栅格矩阵，记录每个栅格是否被占据
#         grid = [[False for _ in range(cols)] for _ in range(rows)]
#         grid_points = [(r, c) for r in range(rows) for c in range(cols)]
#         # print(len(grid))
#         # print(len(grid[0]))
#         # for j in range(num_stations):
#         while len(location_per_run) < num_stations:
#             # 随机生成一个点
#             x = random.uniform(0, world_size)
#             y = random.uniform(0, world_size)
#             point = Point(x, y)
#
#             # 判断点是否在任何一个多边形内,如果在，就将标签置为真
#             in_poly = False
#             for poly in polygons:
#                 if poly.contains(point):
#                     in_poly = True
#                     break
#
#             # 如果点不在任何一个多边形内，将其所在栅格标记为占据，
#             # 这样，只有在城市内的空白栅格才会被选中作为充电站的位置，而城市范围外的点将被忽略。
#             if not in_poly:
#                 row = int(y / grid_size)
#                 col = int(x / grid_size)
#                 if row >= 0 and row < rows and col >= 0 and col < cols:  # 城市范围内的
#                     if not grid[row][col]:
#                         grid[row][col] = True
#                         location_per_run.append((row, col))
#                         # location_per_run.append((x, y, station_capacity))
#         charging_station_locations.append(location_per_run)
#
#     # 返回多轮生成结果
#     return charging_station_locations

from typing import List, Tuple
import geopandas as gpd
import random
from shapely.geometry import Point, Polygon


def generate_charging_station_locations(world_size: int, num_stations: int,
                                        map_file: str, station_capacity: int) -> List[Tuple[float, float, int]]:
    # 读取shp地图数据
    gdf = gpd.read_file(map_file)
    # 获取地图数据范围
    minx, miny, maxx, maxy = gdf.total_bounds
    # 计算地图数据的宽和高
    width = maxx - minx
    height = maxy - miny
    # print(width,height)

    # 计算地图的中心点坐标
    center_x = (maxx + minx) / 2
    center_y = (maxy + miny) / 2
    # 计算正方形世界中的每个格子代表的大小
    # grid_size = 1
    # 即地图数据和世界边界的比例
    ratio = max(width, height) / world_size  # grid_size

    # 计算地图数据放缩到正方形世界后的宽和高，即代表的格子数
    scaled_width = int(width / ratio)
    scaled_height = int(height / ratio)
    # 计算地图数据放缩后的左下角坐标
    scaled_min_col = int((world_size - scaled_width) / 2)
    scaled_min_row = int((world_size - scaled_height) / 2)
    # 获取多边形列表
    polygons = list(gdf.geometry)

    # # 将地图数据栅格化
    # grid_size = max(scaled_width, scaled_height) / world_size
    # rows = int(scaled_height / grid_size)
    # cols = int(scaled_width / grid_size)

    # 生成充电站位置信息
    charging_station_locations = []

    for i in range(NUMBER_OF_REPETITIONS):
        location_per_run = []
        # 创建一个栅格矩阵，记录每个栅格是否被占据
        grid = [[False for _ in range(world_size)] for _ in range(world_size)]
        # grid_points = [(r, c) for r in range(rows) for c in range(cols)]

        while True:
            # 在城市范围内随机生成一个点
            point = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
            # 判断该点是否在城市的边界内
            if any(polygon.contains(point) for polygon in polygons):
                # 将该点转换为栅格坐标,向下取整
                # col = int((point.x / ratio - scaled_minx) / grid_size)
                col = int((point.x - minx) / ratio) + scaled_min_col
                row = int((point.y - miny) / ratio) + scaled_min_row
                # row = int((point.y / ratio - scaled_miny) / grid_size)

                # # 将scaled_minx转换为相同的尺度
                # scaled_minx_grid = scaled_minx / grid_size
                # scaled_miny_grid = scaled_miny / grid_size
                # # 计算充电站在栅格中的位置
                # station_col = int((scaled_minx_grid + world_size / 2) / grid_size)
                # station_row = int((scaled_miny_grid + world_size / 2) / grid_size)

                # 如果该栅格已经被占据，则重新生成一个点
                if grid[row][col]:
                    continue
                # 否则将该栅格标记为已占据，并将该点添加到位置列表中
                grid[row][col] = True
                # location_per_run.append((point.x, point.y, station_capacity))
                location_per_run.append((row, col))
                # 如果已经生成足够的充电站，则退出循环
                if len(location_per_run) == num_stations:
                    break
        # charging_station_locations.extend(location_per_run)
        charging_station_locations.append(location_per_run)

        # while len(location_per_run) < num_stations:
        #     # 城市矩阵范围内随机生成一个点
        #     # x = random.uniform(scaled_minx, scaled_minx + scaled_width)
        #     # y = random.uniform(scaled_miny, scaled_miny + scaled_height)
        #     # point = Point(x, y)
        #     point = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        #
        #     # 计算点在缩放后的坐标系中的坐标
        #     scaled_x = (point.x - minx) / ratio
        #     scaled_y = (point.y - miny) / ratio
        #
        #     # 判断点是否在任何一个多边形内,如果在，就将标签置为真
        #     in_poly = False
        #     for poly in polygons:
        #         if poly.contains(point):
        #             in_poly = True
        #             row = int((scaled_y - scaled_miny) / grid_size)
        #             col = int((scaled_x - scaled_minx) / grid_size)
        #             # if row >= 0 and row < rows and col >= 0 and col < cols:  # 城市范围内的
        #             if not grid[row][col]:
        #                 grid[row][col] = True
        #                 # location_per_run.append((x, y, station_capacity))
        #                 location_per_run.append((row, col))
        #
        #     # 如果点不在任何一个多边形内，将其所在栅格标记为占据，
        #     # 这样，只有在城市内的空白栅格才会被选中作为充电站的位置，而城市范围外的点将被忽略。
        #     if not in_poly:
        #         break
        #         # continue
        # charging_station_locations.append(location_per_run)

    return charging_station_locations


# def read_shapefile(shapefile_path, world_size):
#     sf = shapefile.Reader(shapefile_path,encoding="latin1")#UTF-8编码报错
#     print(sf)
#     shapes = sf.shapes()
#     records = sf.records()
#
#     polygons = []
#     for i in range(len(shapes)):
#         bbox = shapes[i].bbox
#         min_x, min_y, max_x, max_y = bbox
#         width = max_x - min_x
#         height = max_y - min_y
#         x_center = (max_x + min_x) / 2
#         y_center = (max_y + min_y) / 2
#         scaling_factor = max(width, height)
#         scaled_world_size = world_size / scaling_factor
#         polygon = [(x * scaled_world_size, y * scaled_world_size) for x, y in shapes[i].points]
#         polygons.append((polygon, records[i]))
#
#     return polygons
#
# def generate_charging_station_locations(map_data):
#     """
#     随机生成充电站的位置，mapdata确定边界max_x,max_y，返回充电站坐标的列表
#     """
#     map_data = np.array(map_data)#list转换成numpy数组
#     max_x, max_y = map_data.shape[0], map_data.shape[1]
#     charging_station_locations = np.zeros((NUMBER_OF_REPETITIONS, num_stations, 2), dtype=int)
#
#     # for polygon in map_data:
#     #     max_x, max_y = polygon.bounds[2], polygon.bounds[3]
#     #     min_x, min_y = polygon.bounds[0], polygon.bounds[1]
#     #     # ...
#     #     # random coordinate
#     #     x, y = np.random.randint(0, max_x), np.random.randint(0, max_y)
#     #
#     #     # regenerate coordinate until empty space is found
#     #     while map_data[x, y] == 1:
#     #         x, y = np.random.randint(0, max_x), np.random.randint(0, max_y)
#     #
#     #     charging_station_locations[i, j] = [x, y]
#     #
#     # return charging_station_locations
#
#     for i in range(NUMBER_OF_REPETITIONS):
#         for j in range(num_stations):
#             # random coordinate
#             x, y = np.random.randint(0, max_x), np.random.randint(0, max_y)
#
#             # regenerate coordinate until empty space is found
#             while map_data[x, y] == 1:
#                 x, y = np.random.randint(0, max_x), np.random.randint(0, max_y)
#
#             charging_station_locations[i, j] = [x, y]
#
#     return charging_station_locations


# import shapefile
# from shapely.geometry import Polygon
#
# def read_shapefile(shapefile_path):
#     sf = shapefile.Reader(shapefile_path,encoding="latin1")
#     records = sf.records()
#     shapes = sf.shapes()
#     polygons = []
#     for shape in shapes:
#         polygon = Polygon(shape.points)
#         polygons.append(polygon)
#     return polygons


# def generate_charging_station_locations(world_size, num_repetitions, num_charging_stations, map_data):
#     """
#     根据地图生成充电站位置
#
#     Args:
#         world_size (int): 地图大小
#         num_repetitions (int): 重复次数
#         num_charging_stations (int): 充电站数量
#         map_data (np.array): 栅格化后的地图数据
#
#     Returns:
#         List: 充电站位置列表
#     """
#     charging_station_locations = []
#     for i in range(num_repetitions):
#         location_per_run = []
#         for j in range(num_charging_stations):
#             while True:
#                 # 随机选择一个位置
#                 x = random.randint(0, world_size - 1)
#                 y = random.randint(0, world_size - 1)
#                 # 如果该位置在可用区域内，则添加该位置
#                 if map_data[x, y] == 1 and (x, y) not in location_per_run:
#                     location_per_run.append((x, y))
#                     break
#         charging_station_locations.append(location_per_run)
#
#     return charging_station_locations


# def generate_charging_station_locations():
#
#     charging_station_locations = []
#     for i in range(NUMBER_OF_REPETITIONS):
#         location_per_run = []
#         for j in range(num_stations):
#             while True:
#                 if random.randint(0, 100) < 100 * NORMAL_DISTRIBUTED_DATA_RATE:
#                     x = -1
#                     y = -1
#                     while x < 0 or x >= world_size:
#                         x = int(np.random.normal(int(world_size / 2), int(world_size / 8)))
#                     while y < 0 or y >= world_size:
#                         y = int(np.random.normal(int(world_size / 2), int(world_size / 8)))
#                 else:
#                     x = random.randint(0, world_size - 1)
#                     y = random.randint(0, world_size - 1)
#                 if (x, y) not in location_per_run:
#                     location_per_run.append((x, y))
#                     break
#
#         charging_station_locations.append(location_per_run)
#
#     return charging_station_locations


def generate_charging_stations(env, cs, charging_station_locations):
    charging_stations = []
    for i in range(num_stations):
        charging_stations.append(
            cs(env, charging_station_locations[i][0], charging_station_locations[i][1], i, station_capacity))
    return charging_stations


def generate_cars(ev, env, charging_stations):
    cars = []
    for i in range(NUMBER_OF_TOTAL_CARS):
        cars.append(
            ev(env, world_size, random.randint(0, world_size), random.randint(0, world_size), i, charging_stations,
               ADVICE_FOLLOW_RATE_FOR_NON_NEAREST_CS, NORMAL_DISTRIBUTED_DATA_RATE, NORMAL_CHARGING_FACTOR,
               FAST_CHARGING_FACTOR))
    return cars


def generate_simulation_controller(env, cars, charging_stations):
    return SimulationController(env, cars, charging_stations)


def generate_rc(type_of_rc, env, charging_stations, cars):
    return type_of_rc(env, charging_stations, cars, station_capacity, int(station_capacity * NUMBER_OF_FAST_CHARGERS))


def run_simulate_car_behaviour(type_of_ev, type_of_cs, charging_station_locations):
    monitoring = Monitoring(type_of_ev, INFORMATION_TIME_UNIT_STEP_SIZE, LENGTH_OF_SIMULATION, ENV_ENTIRE_LENGTH,
                            num_stations, NUMBER_OF_TOTAL_CARS, world_size)

    env = simpy.Environment()

    charging_stations = generate_charging_stations(env, type_of_cs, charging_station_locations[0])
    cars = generate_cars(type_of_ev, env, charging_stations)
    simulation_controller = generate_simulation_controller(env, cars, charging_stations)
    env.process(monitoring.save_car_data(env))
    monitoring.initialize_monitoring_process(env, charging_stations, cars)

    env.run(until=LENGTH_OF_SIMULATION)

    return monitoring


def run_simulation(type_of_ev, type_of_cs, charging_station_locations):
    # metrics = Metrics(NUMBER_OF_CARS, num_stations, LENGTH_OF_SIMULATION, NUMBER_OF_REPETITIONS, station_capacity)
    monitoring = Monitoring(type_of_ev, INFORMATION_TIME_UNIT_STEP_SIZE, LENGTH_OF_SIMULATION, ENV_ENTIRE_LENGTH,
                            num_stations, NUMBER_OF_TOTAL_CARS, world_size)

    for i in range(NUMBER_OF_REPETITIONS):
        env = simpy.Environment()

        charging_stations = generate_charging_stations(env, type_of_cs, charging_station_locations[i])
        cars = generate_cars(type_of_ev, env, charging_stations)
        simulation_controller = generate_simulation_controller(env, cars, charging_stations)
        monitoring.initialize_monitoring_process(env, charging_stations, cars)
        monitoring.start_timing(env)

        env.run(until=LENGTH_OF_SIMULATION)
        print("Finished run {}".format(i + 1))

    return monitoring


def run_simulation_with_rc(type_of_ev, type_of_cs, type_of_rc, charging_station_locations):
    monitoring = Monitoring(type_of_ev, INFORMATION_TIME_UNIT_STEP_SIZE, LENGTH_OF_SIMULATION, ENV_ENTIRE_LENGTH,
                            num_stations, NUMBER_OF_TOTAL_CARS, world_size)

    for i in range(NUMBER_OF_REPETITIONS):
        env = simpy.Environment()

        charging_stations = generate_charging_stations(env, type_of_cs, charging_station_locations[i])
        cars = generate_cars(type_of_ev, env, charging_stations)
        rc = generate_rc(type_of_rc, env, charging_stations, cars)
        simulation_controller = generate_simulation_controller(env, cars, charging_stations)
        for car in cars:
            car.get_recommendation_center(rc)

        monitoring.initialize_monitoring_process(env, charging_stations, cars)
        monitoring.start_timing(env)

        env.run(until=LENGTH_OF_SIMULATION)
        print("Finished run {}".format(i + 1))

    return monitoring


def run_simulation_rc_parameters(type_of_ev, type_of_cs, type_of_rc, charging_station_locations, number_of_cars,
                                 number_of_cs, normal_charging_factor, fast_charging_factor, capacity_per_cs):
    monitoring = Monitoring(type_of_ev, INFORMATION_TIME_UNIT_STEP_SIZE, LENGTH_OF_SIMULATION, ENV_ENTIRE_LENGTH,
                            number_of_cs, number_of_cars, world_size)

    for i in range(NUMBER_OF_REPETITIONS):
        env = simpy.Environment()

        charging_stations = generate_charging_stations_parameters(env, type_of_cs, charging_station_locations[i],
                                                                  number_of_cs, capacity_per_cs)
        cars = generate_cars_parameters(type_of_ev, env, charging_stations, normal_charging_factor,
                                        fast_charging_factor)
        rc = generate_rc(type_of_rc, env, charging_stations, cars)
        simulation_controller = generate_simulation_controller(env, cars, charging_stations)
        for car in cars:
            car.get_recommendation_center(rc)

        monitoring.initialize_monitoring_process(env, charging_stations, cars)
        monitoring.start_timing(env)

        env.run(until=LENGTH_OF_SIMULATION)
        print("Finished run {}".format(i + 1))

    return monitoring


def run_simulation_parameters(type_of_ev, type_of_cs, charging_station_locations, number_of_cars, number_of_cs,
                              normal_charging_factor, fast_charging_factor, capacity_per_cs):
    monitoring = Monitoring(type_of_ev, INFORMATION_TIME_UNIT_STEP_SIZE, LENGTH_OF_SIMULATION, ENV_ENTIRE_LENGTH,
                            number_of_cs, number_of_cars, world_size)

    for i in range(NUMBER_OF_REPETITIONS):
        env = simpy.Environment()

        charging_stations = generate_charging_stations_parameters(env, type_of_cs, charging_station_locations[i],
                                                                  number_of_cs, capacity_per_cs)
        cars = generate_cars_parameters(type_of_ev, env, charging_stations, number_of_cars, normal_charging_factor,
                                        fast_charging_factor)
        simulation_controller = generate_simulation_controller(env, cars, charging_stations)

        monitoring.initialize_monitoring_process(env, charging_stations, cars)
        monitoring.start_timing(env)

        env.run(until=LENGTH_OF_SIMULATION)
        print("Finished run {}".format(i + 1))

    return monitoring


def generate_cars_parameters(ev, env, charging_stations, number_of_cars, normal_charging_factor, fast_charging_factor):
    cars = []
    for i in range(number_of_cars):
        cars.append(
            ev(env, world_size, random.randint(0, world_size), random.randint(0, world_size), i, charging_stations,
               ADVICE_FOLLOW_RATE_FOR_NON_NEAREST_CS, NORMAL_DISTRIBUTED_DATA_RATE, normal_charging_factor,
               fast_charging_factor))
    return cars


def generate_charging_stations_parameters(env, cs, charging_station_locations, number_of_cs, capacity_per_cs):
    charging_stations = []
    for i in range(number_of_cs):
        charging_stations.append(
            cs(env, charging_station_locations[i][0], charging_station_locations[i][1], i, capacity_per_cs))
    return charging_stations


def generate_charging_station_locations_parameters(number_of_charging_stations):
    charging_station_locations = []
    for i in range(NUMBER_OF_REPETITIONS):
        location_per_run = []
        for j in range(number_of_charging_stations):
            while True:
                if random.randint(0, 100) < 100 * NORMAL_DISTRIBUTED_DATA_RATE:
                    x = -1
                    y = -1
                    while x < 0 or x >= world_size:
                        x = int(np.random.normal(int(world_size / 2), int(world_size / 8)))
                    while y < 0 or y >= world_size:
                        y = int(np.random.normal(int(world_size / 2), int(world_size / 8)))
                else:
                    x = random.randint(0, world_size - 1)
                    y = random.randint(0, world_size - 1)
                if (x, y) not in location_per_run:
                    location_per_run.append((x, y))
                    break

        charging_station_locations.append(location_per_run)

    return charging_station_locations
