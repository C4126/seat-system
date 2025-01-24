import socket
import threading
seat=[]
def create_server_socket(host, port):
    socket_server = socket.socket()
    socket_server.bind((host, port))
    socket_server.listen(5)
    print(f"服务端已启动，地址{host}，端口{port}")
    print(f"正在等待客户端连接...")
    # 开启多线程，收发来自多个客户端的数据
    global num
    num = 0
    while True:
        conn, address = socket_server.accept()
        print(f"服务端已接受到客户端 {num}号 的连接请求，客户端信息：{address}")
        client_handler = threading.Thread(target=handle_client, args=(conn, address, num))
        client_handler.start()
        num += 1


# 处理收发数据
def handle_client(conn, address, num):
    seat.append([])
    member_num=0
    while True:
        data = conn.recv(1024).decode("Utf-8")
        if data == 'exit':
            break
        if data == '<get_status>':
            print('get_status')
            tmp_string = "<"
            tmp_num = 0
            for i in seat[num]:
                tmp_num += 1
                tmp_string = tmp_string + i
                if tmp_num != 4:
                   tmp_string = tmp_string + ";"
            if tmp_num == 0:
                conn.send("<none>".encode('utf-8'))
                continue
            while tmp_num < 4:
                tmp_num += 1
                tmp_string = tmp_string + "No"
                if tmp_num != 4:
                    tmp_string = tmp_string + ";"
            tmp_string+=">"
            conn.send(tmp_string.encode("UTF-8"))
            continue
        else:
            data = data.replace("<", "")
            data = data.replace(">", "")
            if data in seat[num]:
                print("remove "+data)
                seat[num].remove(data)
                #conn.send("OK".encode("UTF-8"))
                member_num -= 1
                continue
            else:
                if member_num >= 4:
                    print("fail_out")
                    #conn.send("fail_out".encode("UTF-8"))
                    continue
                print("add "+data)
                member_num += 1
                seat[num].append(data)
                #conn.send("OK".encode("UTF-8"))
                continue

def add_member(data):
    for i in range(num):
        if seat[num].len() == 0:
            seat[num].append(data)
            return
    else:
        for i in range(num):
            if seat[num].len() != 4:
                seat[num].append(data)
                return

if __name__ == '__main__':
    server_host = "127.0.0.1"
    server_port = 8888
    create_server_socket(server_host, server_port)