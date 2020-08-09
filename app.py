# coding: utf-8
from flask import Flask, render_template, make_response
# import subscribe
# from subscribe import MySubscriber
import db
import paho.mqtt.client as mqtt
import datetime
# import drawing
import sqlite3

app = Flask(__name__)


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache'
    return response


@app.route('/hello')
def hello():
    name = "Hoge"
    # return name
    return render_template('hello.html', title='flask test', name=name)


@app.route('/good')
def good():
    name = "こんにちは"
    return name


@app.route('/')
def graph():
    full_filename = "./static/graph_sensor1.png"
    return render_template("graph.html", user_image=full_filename)


mydb = db.MyDB()
print(mydb)


# ブローカーに接続できたときの処理
def on_connect(client, userdata, flag, rc):
    print("Connected with result code " + str(rc))  # 接続できた旨表示
    client.subscribe("esp32")  # subするトピックを設定


# ブローカーが切断したときの処理
def on_disconnect(client, userdata, flag, rc):
    if rc != 0:
        print("Unexpected disconnection.")


# メッセージが届いたときの処理
def on_message(client, userdata, msg):
    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    # msg.topicにトピック名が，msg.payloadに届いたデータ本体が入っている
    print(now_str + " Received message '" + str(msg.payload) + "' on topic '" + msg.topic + "' with QoS " + str(
        msg.qos))
    temp, hum = map(int, msg.payload.split())
    # print(str(temp) + " " + str(hum))
    temp /= 10.0
    hum /= 10.0
    global mydb
    # print(mydb)
    with sqlite3.connect(db.db_path) as con:
        data = (now_str, temp, hum)
        cur = con.cursor()
        cur.execute("INSERT INTO sensor1 VALUES (?,?,?)", data)
        con.commit()

        mydb.d_date.append(now_str)
        mydb.d_temp.append(temp)
        mydb.d_hum.append(hum)
    # mydb.insert_data(now_str, temp, hum)  # DBに追記
    # mydb.update_list()

    mydb.update_graph()
    # drawing.update_graph(mydb)
    # with plt.figure(figsize=(6, 4)) as fig:
    #     pass
        # ax = fig.add_subplot(111)
        #
        # # d_date, d_temp, d_hum = mydb.get_lists()
        #
        # ax.plot(mydb.d_date, mydb.d_temp)
        # ax.plot(mydb.d_date, mydb.d_hum)
        # # plt.show()
        # fig.savefig("./static/graph_sensor1.png")


def start_mqtt(client_):
    # MQTTの接続設定
    # client = mqtt.Client()  # クラスのインスタンス(実体)の作成
    client_.on_connect = on_connect  # 接続時のコールバック関数を登録
    client_.on_disconnect = on_disconnect  # 切断時のコールバックを登録
    client_.on_message = on_message  # メッセージ到着時のコールバック

    client_.connect("localhost", 8888, 60)  # 接続先は自分自身

    # client.loop_forever()                  # 永久ループして待ち続ける
    client_.loop_start()


# if __name__ == "__main__":
client = mqtt.Client()  # クラスのインスタンス(実体)の作成
mydb.init_datalist()
# subscriber = MySubscriber()
start_mqtt(client)
# subscribe.start_mqtt()

app.run(debug=False, host='xxx.xxx.xxx.xxx', port=80)
# app.run()
