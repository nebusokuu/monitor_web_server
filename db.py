import sqlite3
from collections import deque
import matplotlib
matplotlib.use('Agg') # -----(1)
# matplotlib.rcParams['font.family']='VL Gothic'
# matplotlib.rcParams['font.size']=12 # フォントサイズを指定
from matplotlib import pyplot as plt
import japanize_matplotlib  
import numpy as np

db_path = 'dblec.sqlite'


class MyDB:
    # データベースファイルのパス
    db_path = 'dblec.sqlite'
    # num_sensor = 1
    # table = "sensor" + str(num_sensor)

    d_date = deque(maxlen=101)
    d_temp = deque(maxlen=101)
    d_hum = deque(maxlen=101)

    def __init__(self):
        # データベース接続とカーソル生成
        self.connection = sqlite3.connect(self.db_path)
        # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
        self.connection.isolation_level = None
        self.cursor = self.connection.cursor()
        self.init_datalist()

    # def insert_data(self, date, temp, hum):
    #     data = (date, temp, hum)
    #     print(temp)
    #     try:
    #         self.cursor.execute("INSERT INTO sensor1 VALUES (?,?,?)", data)
    #         self.connection.commit()
    #     except sqlite3.Error as e:
    #         print('sqlite3.Error occurred:', e.args[0])
    #     print(temp)  # これが表示されない

        # print(get_lastrow())

    # def get_table(self):
    #     self.cursor.execute("SELECT * FROM sensor1 ORDER BY temp DESC LIMIT 5")
    #     table_list = [_row for _row in self.cursor.execute("SELECT * FROM sensor1 ORDER BY temp DESC LIMIT 5")]
    #     return table_list

    def get_lastrow(self):
        return self.cursor.execute("SELECT * FROM sensor1 ORDER BY date DESC LIMIT 1").fetchone()

    def init_datalist(self):
        num_row = self.cursor.execute("select count(*) from sensor1").fetchone()[0]
        if num_row > 101:
            num_row = 101

        for data in self.cursor.execute("SELECT * FROM sensor1 ORDER BY date DESC LIMIT " + str(num_row)):
            self.d_date.appendleft(data[0])
            self.d_temp.appendleft(data[1])
            self.d_hum.appendleft(data[2])

    def update_graph(self):
        # fig = plt.figure(figsize=(6, 4))
        fig = plt.figure()
        # ax = fig.add_subplot(111)

        # d_date, d_temp, d_hum = mydb.get_lists()

        fig.subplots_adjust(bottom=0.2)

        plt.title('自室の気温と湿度  最終更新:' + self.d_date[-1])
        plt.axis("off")

        # figureオブジェクトに属するaxesオブジェクトを生成
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)

        plt.subplots_adjust(hspace=1)

        # それぞれのaxesオブジェクトのlines属性にLine2Dオブジェクトを追加
        ax1.plot(self.d_date, self.d_temp, label="Temperature(°C)", color="orange")
        ax2.plot(self.d_date, self.d_hum, label="Humidity(%)", color="b")

        ax1.set_ylim([0, 50])
        ax2.set_ylim([0, 100])

        start, end = ax1.get_xlim()
        ax1.xaxis.set_ticks(np.arange(start, end, 20))
        labels = ax1.get_xticklabels()
        plt.setp(labels, rotation=45, fontsize=7)
        start, end = ax2.get_xlim()
        ax2.xaxis.set_ticks(np.arange(start, end, 20))
        labels = ax2.get_xticklabels()
        plt.setp(labels, rotation=45, fontsize=7)
        # ax1.ticklabels(axis='x', labelrotation=90)
        # ax1.set_xticklabels(rotation=90)
        # plt.xticks(x[::4], dt_labels[::4], rotation=90, size='small')


        # 凡例をつける
        ax1.legend()
        ax2.legend()

        # ax.plot(self.d_date, self.d_temp, label="Temperature", color="orange")
        # ax.plot(self.d_date, self.d_hum,  label="Humidity", color="b")
        # ax.set_ylim([0, 100])
        # # 凡例を表示
        # ax.legend()

        # plt.show()
        fig.savefig("./static/graph_sensor1.png")
        fig.close()

    # def update_list(self):
    #     print(2)
    #     print(self.get_lastrow())
    #     lastdata = self.get_lastrow()
    #     print(lastdata[0])
    #     print(lastdata[1])
    #     print(lastdata[2])
    #     self.d_date.append(lastdata[0])
    #     self.d_temp.append(lastdata[1])
    #     self.d_hum.append(lastdata[2])

    def get_lists(self):
        return self.d_date, self.d_temp, self.d_hum

# # データベースファイルのパス
# db_path = 'dblec.sqlite'
#
# num_sensor = 1
#
# table = "sensor" + str(num_sensor)
#
# # データベース接続とカーソル生成
# connection = sqlite3.connect(db_path)
# # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
# connection.isolation_level = None
# cursor = connection.cursor()
#
#
# def insert_data(date, temp, hum):
#     data = (date, temp, hum)
#     print(temp)  # この上の2行が悪さ
#     cursor.execute("INSERT INTO sensor1 VALUES (?,?,?)", data)
#     connection.commit()
#     print(temp)  # この上の2行が悪さ
#
#     # print(get_lastrow())
#
# def get_table():
#     cursor.execute("SELECT * FROM sensor1 ORDER BY temp DESC LIMIT 5")
#     table_list = [_row for _row in cursor.execute("SELECT * FROM sensor1 ORDER BY temp DESC LIMIT 5")]
#     return table_list
#
#
# def get_lastrow():
#     return cursor.execute("SELECT * FROM sensor1 ORDER BY date DESC LIMIT 1").fetchone()
#
#
# d_date = deque(maxlen=100)
# d_temp = deque(maxlen=100)
# d_hum = deque(maxlen=100)
#
#
# def init_datalist():
#     num_row = cursor.execute("select count(*) from sensor1").fetchone()[0]
#     if num_row > 100:
#         num_row = 100
#
#     for data in cursor.execute("SELECT * FROM sensor1 ORDER BY date DESC LIMIT " + str(num_row)):
#         d_date.appendleft(data[0])
#         d_temp.appendleft(data[1])
#         d_hum.appendleft(data[2])


# def update_list():
#     lastdata = get_lastrow()
#     d_date.append(lastdata[0])
#     d_temp.append(lastdata[1])
#     d_hum.append(lastdata[2])
#
#
# def get_lists():
#     return d_date, d_temp, d_hum
#

# if __name__ == "__main__":
#     init_datalist()
#
#     import matplotlib.pyplot as plt
#
#     insert_data(5,5,5)
#
#     fig = plt.figure(figsize=(12, 8))
#     ax = fig.add_subplot(111)
#     ax.plot(d_date, d_temp)
#     ax.plot(d_date, d_hum)
#     plt.show()
#     fig.savefig("./static/graph_sensor1.png")
#
#     print(d_date)
