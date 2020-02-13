import numpy as np

from config import *

class Hospital(object):
    def __init__(self):
        self.bed_num = BED_NUM # 床位
        self.beds = np.empty(shape=(0, 3), dtype=int)
        # 床位矩阵
        bed_matrix_line = int(self.bed_num / 20) # 行
        bed_matrix_column = int(self.bed_num / bed_matrix_line) # 列
        for i in range(bed_matrix_column):
            for j in range(bed_matrix_line):
                bed = [[i, j, IDLE_STATU]]
                self.beds = np.r_[self.beds, bed]

    def get_bed(self):
        # 空床位的行号
        try:
            bed_line = np.where(self.beds[:, 2] == 0)[0][0]
            self.beds[bed_line, 2] = OCCUPY_STATUS # 占用
            return self.beds[bed_line]
        except:
            return np.array([]) # 没有床位


    def get_x(self):
        return self.beds[:, 0]

    def get_y(self):
        return self.beds[:, 1]

    def get_bed_status(self):
        '''
        获得床位状态
        :return:
        '''
        return self.beds[:, 2]