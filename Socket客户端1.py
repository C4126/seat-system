import socket


def create_client(host, port):
    socket_client = socket.socket()
    socket_client.connect((host, port))
    # 发送、接受数据
    while True:
        msg = input(f"请输入客户端1发送给服务端{host}:{port}的数据：")
        if msg == "exit":
            break
        # 发送数据到服务端
        socket_client.send(msg.encode("UTF-8"))
        # 接收服务端的数据
        data_from_server = socket_client.recv(1024).decode("UTF-8")
        print(f"客户端接收到服务端的消息：{data_from_server}")
    socket_client.close()

if __name__ == '__main__':
    host = "127.0.0.1"
    port = 8888
    create_client(host, port)