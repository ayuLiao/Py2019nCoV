'''
人的状态：
    0 未感染
    1 潜伏期
    2 确诊
    3 隔离（住院，会占用床位）
    4 免疫期
    5 死亡
'''

# 概率分布标准差
SCALE = 1

'''
基本配置
'''
INFECTION_NUM = 100 # 初始感染人数
LATENT_TIME = 14 # 潜伏期
THEATMENT_TIME = 10 # 治疗时间
IMMUNE_TIME = 30 # 免疫期
HOSPITAL_TIME = 3 # 医院收治时间 （发现后入院所需的时间）

SPREAD_RATE = 0.8 # 传播率（正常人接触感染者被感染的概率）
DEATH_RATE = 0.02 # 死亡率
ACTION_RATE = 1 # 行动意向，是否出去走走

SAFETY_AWARENESS = 10 # 安全意识 -> [0.001 ~ 10] 安全意识越强，疫情越容易受到控制
SECURITY_DIST = 50 # 安全距离（正常人与感染者的距离小于50，则可能会被感染）
CITY_PEOPLE_NUM = 10000 # 城市人数
SCALE = 1000 # 规模

'''
人的状态
'''
#     0 未感染
#     1 潜伏期
#     2 确诊
#     3 隔离（住院，会占用床位）
#     4 免疫期
#     5 死亡
UNINFECTED_STATUS = 0
LATENT_STATUS = 1
CONFIRMED_STATUS = 2
ISOLATION_STATUS = 3
IMMUNE_STATUS = 4
DEATH_STATUS = 5

'''
床位状态
'''
#     0 闲置
#     1 占用
IDLE_STATU = 0
OCCUPY_STATUS = 1


'''
医院相关
'''

BED_NUM = 1000 # 床位

'''
画布相关
'''
# 画布的起点
CANVAS_INIT = (0, 0)

# 人在不同状态对应的颜色
PEOPLE_COLORS = [
    'white', # 未感染
    'yellow', # 潜伏期
    'red',  # 确诊
    'black', # 隔离
    'green', # 免疫期
    'black', # 死亡
    'purple', # 绘制隔离曲线
    'grey', # 绘制死亡曲线
]

# 医院床位不同状态的颜色
BED_COLORS = [
    'black', # 空床
    'red', # 有人
]