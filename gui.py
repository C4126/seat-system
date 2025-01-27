import socket
import threading
import tkinter as tk
from tkinter import ttk

# 定义全局变量seat
seat = []
mapping = {"25-175-62-2": "Alex","46-192-199-1": "Bob"}
num = 0
def create_server_socket(host, port):
    socket_server = socket.socket()
    socket_server.bind((host, port))
    socket_server.listen(5)
    print(f"服务端已启动，地址{host}，端口{port}")
    print(f"正在等待客户端连接...")
    # 开启多线程，收发来自多个客户端的数据
    global num
    while True:
        conn, address = socket_server.accept()
        print(f"服务端已接受到客户端 {num}号 的连接请求，客户端信息：{address}")
        client_handler = threading.Thread(target=handle_client, args=(conn, address, num))
        client_handler.start()
        #num += 1

def add_member(data):
    global num
    for i in range(num):
        #先在已有的桌子间寻找空桌子加入
        if len(seat[i]) == 0:
            seat[i].append(mapping[data])
            return
    else:
        #若没有则从一号起寻找未满员的桌子加入
        for i in range(num):
            if len(seat[i]) != 4:
                seat[i].append(mapping[data])
                return

# 处理收发数据
def handle_client(conn, address, anum):
    global num
    data = conn.recv(1024).decode("Utf-8")
    data = data.replace("<", "")
    data = data.replace(">", "")
    # data = data.replace("\n", "")
    if data=="!":
        conn.send("主机".encode("UTF-8"))
        while True:
            data = conn.recv(1024).decode("Utf-8")
            data = data.replace("<", "")
            data = data.replace(">", "")
            # data = data.replace("\n", "")
            if data == 'exit':
                break
            if data == "":
                continue
            else:
                add_member(data)
                print("add "+data)
                conn.send("OK".encode("UTF-8"))
    else:
        num += 1
        conn.send("客机".encode("UTF-8"))
        seat.append([])
        member_num = 0
        while True:
            data = conn.recv(1024).decode("Utf-8")
            while "<" not in data:
                data = data.replace("<", "")
                data = data.replace(">", "")
            #data = data.replace("\n", "")
            if data == '':
                continue
            else:
                if data == 'exit':
                    break
                if 'get_status' in data:
                    print('get_status')
                    tmp_string = "<"
                    tmp_num = 0
                    # 遍历seat[num]，将每个元素添加到tmp_string中
                    for i in seat[anum]:
                        tmp_num += 1
                        tmp_string = tmp_string + i
                        if tmp_num != 4:
                           tmp_string = tmp_string + ";"
                    #若桌子人数不足4人，则添加No至四个元素
                    while tmp_num < 4:
                        tmp_num += 1
                        tmp_string = tmp_string + "No"
                        if tmp_num != 4:
                            tmp_string = tmp_string + ";"
                    tmp_string += ">"
                    conn.send(tmp_string.encode("UTF-8"))
                    continue
                while "get_status" not in data:
                    data = data.replace("get_status", "")
                data = mapping[data]
                #若桌中中已有该人，则删除该人并返回OK
                if data in seat[anum]:
                    print("remove " + data)
                    seat[anum].remove(data)
                    conn.send("OK".encode("UTF-8"))
                    member_num -= 1
                    continue
                else:
                    #判断桌子是否满员，若是则返回fail_out
                    if member_num >= 4:
                        print("fail_out")
                        conn.send("fail_out".encode("UTF-8"))
                        continue
                    #添加该人并返回OK
                    print("add " + data)
                    member_num += 1
                    seat[anum].append(data)
                    conn.send("OK".encode("UTF-8"))
                    continue
        conn.close()

def update_seat_display():
    #更新seat数组的显示
    for i, row in enumerate(seat):
        if i < len(seat_display):
            seat_display[i].config(text=str(row))
        else:
            label = ttk.Label(root, text=str(row))
            label.pack(pady=5)
            seat_display.append(label)
    root.after(50, update_seat_display)  # 每隔50ms调用一次

def create_gui():
    #创建GUI窗口
    global root, seat_display

    root = tk.Tk()
    root.title("Seat Status")

    seat_display = []
    update_seat_display()  # 启动更新显示
    root.mainloop()

if __name__ == '__main__':
    # 启动GUI线程
    gui_thread = threading.Thread(target=create_gui)
    gui_thread.start()

    # 配置并启动socket
    server_host = "127.0.0.1"
    server_port = 8888
    create_server_socket(server_host, server_port)
