world_size = 5000 # 模拟城市的尺寸，正方形

num_stations = 30   # 充电站数量
station_capacity = 15    # 每个充电站的充电桩数量
NUMBER_OF_TOTAL_CARS = 600    # 城市中运行的电动车数量

ENV_ENTIRE_LENGTH = 259200    # 单个车模拟时间的总长度，也就是这辆车持续活跃的时间，单位是秒；这里按48小时
LENGTH_OF_SIMULATION = 432000    # 单次模拟的时间长度，单位是秒，这里是120小时
NUMBER_OF_REPETITIONS = 10    # 每个策略运行的模拟次数 (MIN: 2)

INFORMATION_TIME_UNIT_STEP_SIZE = 500    # 绘图分析的信息记录的时间间隔，单位是秒
ADVICE_FOLLOW_RATE_FOR_NON_NEAREST_CS = 0.9   # 如果系统推荐的不是最近的充电站，用户听从系统建议的概率(MIN: 0, MAX: 1)
NORMAL_DISTRIBUTED_DATA_RATE = 0.3   # 正态分布的车辆和充电站的比例(MIN: 0, MAX: 1)

NUMBER_OF_FAST_CHARGERS = 0.4    # 快充桩占全部充电桩的比例 (MIN: 0, MAX: 1)
NORMAL_CHARGING_FACTOR = 0.6   # 常规充电桩充满一辆车需要的时间
FAST_CHARGING_FACTOR = 0.1   # 快充桩充满一辆车需要的时间

TIME_FACTOR = {     # 各小时城市里运行的平均车辆数占总车辆数的比例
    0: 0.5,
    1: 0.4,
    2: 0.3,
    3: 0.25,
    4: 0.4,
    5: 0.55,
    6: 0.7,
    7: 0.95,#高峰期
    8: 0.95,
    9: 0.95,
    10: 0.9,
    11: 0.85,
    12: 0.8,
    13: 0.8,
    14: 0.75,
    15: 0.75,
    16: 0.85,#高峰期
    17: 0.95,
    18: 0.95,
    19: 0.95,
    20: 0.75,
    21: 0.65,
    22: 0.55,
    23: 0.45
}
