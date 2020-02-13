import numpy as np
from scipy.spatial.distance import cdist as scipy_cdist

from hospital import Hospital
from config import *

class Peoples(object):
    def __init__(self, hospital):
        self.hospital = hospital

        self.conf = {
            'x': 0, # x坐标
            'y': 1, # y坐标
            'status':2, # 状态
            'infected_time': 3, # 潜伏时间
            'confirmed_time': 4, # 确诊时间
            'bed': 5, # 使用医院床位隔离治疗
            'hospital_time': 6, # 住院隔离时间
            'immune_time': 7, # 免疫时间
        }

        # people = [[x, y, status, infected_time, confirmed_time, bed, hospital_time, immune_time]]
        self.peoples = np.empty(shape=(0, 8), dtype=object)
        # 初始化people位置与状态
        for i in range(CITY_PEOPLE_NUM):
            # 使用正态分布随机生成
            x = SCALE * np.random.normal(0, 1) + CANVAS_INIT[0]
            y = SCALE * np.random.normal(0, 1) + CANVAS_INIT[1]
            people = [[x, y, UNINFECTED_STATUS, 0, 0, 0, 0, 0]]
            self.peoples = np.r_[self.peoples, people]

    def init(self):
        '''
        初始化 INFECTION_NUM 个感染者
        :return:
        '''
        for i in range(INFECTION_NUM):
            index = np.random.randint(0, CITY_PEOPLE_NUM)
            self.peoples[index][self.conf['status']] = LATENT_STATUS


    def getCoordinate(self):
        '''
        获得people坐标
        :return: numpy array
        '''
        return self.peoples[:, [self.conf['x'], self.conf['y']]]

    def get_x(self):
        return self.peoples[:, self.conf['x']]

    def get_y(self):
        return self.peoples[:, self.conf['y']]

    def get_people_status(self):
        '''获得人的状态'''
        return self.peoples[:, self.conf['status']]

    def uninfected_people(self, coord_dists, index, people, time, spead_rate):
        '''
        未感染者
        :param coord_dists: 距离矩阵
        :param index: 某个人在矩阵的index
        :param people: 具体的某个人
        :param time: 时间，Matplotlib animation 的 帧
        :return:
        '''
        # 邻居，如果邻居中存在感染者，可能被感染
        neighbors = np.where(coord_dists[index] < SECURITY_DIST)[0]
        for i in neighbors:
            status = self.conf['status']
            # 潜伏期 或 确诊（没有被隔离）可以感染他人
            if self.peoples[i][status] == LATENT_STATUS or \
                    self.peoples[i][status] == CONFIRMED_STATUS:
                if np.random.rand() < spead_rate:  # 取随机数，小于传播率，则被感染
                    people[self.conf['infected_time']] = time # 感染时间
                    people[status] = LATENT_STATUS # 潜伏期
        return people

    def latent_people(self, people, time, latent_time, index):
        '''
        潜伏期患者
        :param people:
        :param time:
        :param latent_time:
        :return:
        '''
        # 当前时间 - 感染时间 > 潜伏时间，此时症状会明显，可以到医院确诊
        if (time - people[self.conf['infected_time']]) > latent_time[index][0]:
            people[self.conf['confirmed_time']] = time # 确诊时间
            people[self.conf['status']] = CONFIRMED_STATUS # 确诊
        return people

    def confirmed_pepole(self, people, time, death_rate):
        '''
        确诊患者
        :param people:
        :param time:
        :return:
        '''
        # 死亡
        if np.random.rand() < death_rate:
            people[self.conf['status']] = DEATH_STATUS
        elif (time - people[self.conf['confirmed_time']]) > HOSPITAL_TIME:
            # 如果有床位，进行治疗
            bed = self.hospital.get_bed()
            if len(bed) != 0:
                people[self.conf['bed']] = bed
                people[self.conf['status']] = ISOLATION_STATUS # 隔离
                people[self.conf['hospital_time']] = time
        return people

    def isolation_people(self, people, time, theatment_time, index, death_rate):
        '''
        隔离患者
        :param people:
        :param time:
        :param theatment_time:
        :param index:
        :return:
        '''
        # 死亡，住院后，死亡率降低10倍
        if np.random.rand() < death_rate / 10:
            people[self.conf['status']] = DEATH_STATUS
            people[self.conf['bed']][2] = IDLE_STATU # 归还床位，为空
            people[self.conf['bed']] = 0

        # 当前时间 - 住院时间 大于 治愈时间
        elif (time - people[self.conf['hospital_time']]) > theatment_time[index][0]:
            people[self.conf['status']] = IMMUNE_STATUS # 进入免疫期
            people[self.conf['immune_time']] = time
            people[self.conf['bed']][2] = IDLE_STATU  # 归还床位，为空
            people[self.conf['bed']] = 0
            people[self.conf['infected_time']]= 0
            people[self.conf['confirmed_time']] = 0
            people[self.conf['hospital_time']] = 0
        return people

    def immune_people(self, people, time, immune_time, index):
        # 当前时间 - 免疫期 > 平均免疫期
        if (time - people[self.conf['immune_time']]) > immune_time[index][0]:
            people[self.conf['status']] = UNINFECTED_STATUS
            people[self.conf['immune_time']] = 0
        return people

    def update(self, time):
        sa = np.exp(-SAFETY_AWARENESS) # 安全意识
        spead_rate = SPREAD_RATE * sa # 感染率

        death_rate = DEATH_RATE * sa # 死亡率

        #  平均潜伏时间
        latent_time = np.random.normal(LATENT_TIME, SCALE, size=(CITY_PEOPLE_NUM, 1))
        # 平均治疗时间
        theatment_time = np.random.normal(THEATMENT_TIME, SCALE, size=(CITY_PEOPLE_NUM, 1))
        # 平均免疫期
        immune_time = np.random.normal(IMMUNE_TIME, SCALE, size=(CITY_PEOPLE_NUM, 1))

        coord = self.getCoordinate()
        # 计算坐标矩阵的欧式距离
        coord_dists = scipy_cdist(coord, coord)
        status = self.conf['status']
        for index, people in enumerate(self.peoples):
            if people[status] == UNINFECTED_STATUS:
                people = self.uninfected_people(coord_dists, index, people, time, spead_rate)
            elif people[status] == LATENT_STATUS:
                people = self.latent_people(people, time, latent_time, index)
            elif people[status] == CONFIRMED_STATUS:
                people = self.confirmed_pepole(people, time, death_rate)
            elif people[status] == ISOLATION_STATUS:
                people = self.isolation_people(people, time, theatment_time, index, death_rate)
            elif people[status] == IMMUNE_STATUS:
                people = self.immune_people(people, time, immune_time, index)

        x = self.conf['x']
        y = self.conf['y']
        action_rate = ACTION_RATE * sa  # 行动意向
        # 走动
        self.peoples[:, [x, y]] += action_rate * SCALE * np.random.randn(CITY_PEOPLE_NUM, 2) / 50

    def run(self, time, rlock):
        rlock.acquire()  # 获得锁
        self.update(time)
        rlock.release()  # 释放锁
