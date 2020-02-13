'''
城市画布
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

from peoples import Peoples
from hospital import Hospital
from config import *

class Canvas(object):
    def __init__(self, peoples):
        self.peoples = peoples
        self.hospital = peoples.hospital
        # 创建画布
        self.fig = plt.figure(figsize=(16, 8))
        plt.style.use('dark_background') # 背景
        self.fig.patch.set_facecolor('black') # 补丁颜色
        # 指定字体
        self.myfont = FontProperties(fname='SimHei.ttf')

        # 创建网格布局
        grid = plt.GridSpec(4, 6, wspace=0.5, hspace=0.3)

        # 创建子图并按网格布局分布
        self.subplots = [
            plt.subplot(grid[0:4, 0:4]),
            plt.subplot(grid[0:4, 4]),
            plt.subplot(grid[0, 5]),
            plt.subplot(grid[1, 5]),
            plt.subplot(grid[2, 5]),
            plt.subplot(grid[3, 5]),
        ]

        # 初始化绘制折线图所需数据结构
        self.init_line()

        # plt.show()

    def count_status(self):
        '''
        计算状态
        :return:
        '''
        peoples_status = self.peoples.get_people_status()
        hospital_status = self.hospital.get_bed_status()

        uninfecated_num = np.sum(peoples_status == UNINFECTED_STATUS) # 未感染人数
        letent_num = np.sum(peoples_status == LATENT_STATUS)  # 潜伏期人数
        confirmed_num = np.sum(peoples_status == CONFIRMED_STATUS)  # 确诊人数
        isolation_num = np.sum(peoples_status == ISOLATION_STATUS)  # 隔离人数
        immune_num = np.sum(peoples_status == IMMUNE_STATUS)  # 免疫人数
        death_num = np.sum(peoples_status == DEATH_STATUS)  # 死亡人数

        bed_num = np.sum(hospital_status == OCCUPY_STATUS) # 被占用床位

        dangerous_people_num = confirmed_num + bed_num # 危险人数，有些确诊人可能没有床位

        return peoples_status, hospital_status, uninfecated_num, \
            letent_num, confirmed_num, isolation_num, \
            immune_num, death_num, bed_num, dangerous_people_num

    def draw_ax0(self,
                 ax0,
                 peoples_status,
                 time,
                 uninfecated_num,
                 letent_num,
                 confirmed_num,
                 isolation_num,
                 immune_num,
                 death_num,
                 dangerous_people_num
                 ):
        '''
        绘制人口散点图，图中不同的颜色表示不同状态的人
        :param ax0: 子图 ax0
        :param peoples_status: 人的状态，根据状态绘制不同的颜色
        :return:
        '''
        ax0.clear()
        ax0.scatter(
            self.peoples.get_x(),
            self.peoples.get_y(),
            c=[PEOPLE_COLORS[int(i)] for i in peoples_status],
            marker='.',  # 绘制 点
            alpha=0.6,
            s=10
        )

        title = f'''时间：{time}，未感染人数：{uninfecated_num}，潜伏期人数：{letent_num}，
                    确诊人数：{confirmed_num}， 隔离人数：{isolation_num}，免疫人数：{immune_num}，
                    死亡人数：{death_num}，高危人员数：{dangerous_people_num}，
                    '''
        ax0.set_title(title, fontproperties=self.myfont)
        # 重铺坐标
        ax0.set_xticks([])
        ax0.set_yticks([])

    def draw_ax1(self, ax1, hospital_status, bed_num):
        '''
        绘制医院床位变化
        :param ax1:
        :param hospital_status: 医院床位状态
        :return:
        '''
        ax1.clear()
        ax1.scatter(
            self.hospital.get_x(),
            self.hospital.get_y(),
            c=[BED_COLORS[int(i)] for i in hospital_status],
            marker='.',  # 绘制 点
            s=10
        )
        title = f'''占用病床百分比：{bed_num/BED_NUM}'''
        ax1.set_title(title, fontproperties=self.myfont)
        ax1.set_xticks([])
        ax1.set_yticks([])

    def draw_line(self, ax, time, data, color, title):
        '''
        绘制线性图
        :return:
        '''
        if time > 0:
            ax.plot([time-1, time], data, color=color)
            ax.set_title(title, fontproperties=self.myfont)
            ax.set_xticks([])
            ax.set_yticks([])

    def init_line(self):
        '''初始化绘制折现的数据'''
        self.latent_data = [0, 0]
        self.confirmed_data = [0, 0]
        self.isolation_num_data = [0, 0]
        self.immune_num_data = [0, 0]
        self.death_data = [0, 0]
        self.dangerous_data = [0, 0]

    def draw_ax2(self, ax2, time, letent_num, confirmed_num):
        self.latent_data[1] = letent_num
        self.confirmed_data[1] = confirmed_num
        title = '潜伏人数与确诊人数变化曲线'
        self.draw_line(ax2, time, self.latent_data, PEOPLE_COLORS[1], title)
        self.draw_line(ax2, time, self.confirmed_data, PEOPLE_COLORS[2], title)
        ax2.set_title(title, fontproperties=self.myfont, fontsize=10)
        self.latent_data[0] = letent_num
        self.confirmed_data[0] = confirmed_num

    def draw_ax3(self, ax3, time, isolation_num, immune_num):
        '''隔离人数与免疫人数变化曲线'''
        self.isolation_num_data[1] = isolation_num # 动图
        self.immune_num_data[1] = immune_num
        title = '隔离人数与免疫人数变化曲线'
        self.draw_line(ax3, time, self.isolation_num_data, PEOPLE_COLORS[6], title)
        self.draw_line(ax3, time, self.immune_num_data, PEOPLE_COLORS[4], title)
        ax3.set_title(title, fontproperties=self.myfont, fontsize=10)
        self.isolation_num_data[0] = isolation_num
        self.immune_num_data[0] = immune_num

    def draw_ax4(self, ax4, time, death_num):
        self.death_data[1] = death_num
        title = '死亡人数变化曲线'
        self.draw_line(ax4, time, self.death_data, PEOPLE_COLORS[7], title)
        ax4.set_title(title, fontproperties=self.myfont, fontsize=10)
        self.death_data[0] = death_num

    def draw_ax5(self, ax5, time, dangerous_people_num):
        self.dangerous_data[1] = dangerous_people_num
        title = '高危人数变化曲线'
        self.draw_line(ax5, time, self.dangerous_data, PEOPLE_COLORS[7], title)
        ax5.set_title(title, fontproperties=self.myfont, fontsize=10)
        self.dangerous_data[0] = dangerous_people_num

    def animate(self, time):
        peoples_status, hospital_status, uninfecated_num, \
        letent_num, confirmed_num, isolation_num, \
        immune_num, death_num, bed_num, dangerous_people_num = self.count_status()
        self.draw_ax0(self.subplots[0], peoples_status, time, uninfecated_num, letent_num,
                      confirmed_num, isolation_num, immune_num, death_num, dangerous_people_num)
        self.draw_ax1(self.subplots[1], hospital_status, bed_num)

        self.draw_ax2(self.subplots[2], time, letent_num, confirmed_num)
        self.draw_ax3(self.subplots[3], time,isolation_num, immune_num)
        self.draw_ax4(self.subplots[4], time, death_num)
        self.draw_ax5(self.subplots[5], time, dangerous_people_num)

    def run(self, time, rlock):
        rlock.acquire() # 获得锁
        self.animate(time)
        rlock.release() # 释放锁


def test():
    canvas = Canvas()
    canvas.animate(1)

if __name__ == '__main__':
    test()
