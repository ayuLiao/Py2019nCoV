'''
2019-nCoV 病毒扩展仿真程序

'''

from threading import Thread, RLock

import matplotlib.pyplot as plt
from matplotlib import animation


from canvas import Canvas
from peoples import Peoples
from hospital import Hospital

def main():
    hospital = Hospital()
    peoples = Peoples(hospital)
    canvas = Canvas(peoples)
    canvas.peoples.init() # 初始化感染者

    def run(time):
        lock = RLock()
        canvas.peoples.run(time, lock)
        canvas.run(time, lock)
        return 0

    ani = animation.FuncAnimation(fig=canvas.fig, func=run, repeat=False)
    plt.show()

if __name__ == '__main__':
    main()
