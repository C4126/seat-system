import socket
import threading


def create_server_socket(host, port):
    socket_server = socket.socket()
    socket_server.bind((host, port))
    socket_server.listen(5)
    print(f"服务端已启动，地址{host}，端口{port}")
    print(f"正在等待客户端连接...")
    # 开启多线程，收发来自多个客户端的数据
    num = 0  # 标记客户端的编号
    while True:
        num += 1
        conn, address = socket_server.accept()
        print(f"服务端已接受到客户端 {num}号 的连接请求，客户端信息：{address}")
        client_handler = threading.Thread(target=handle_client, args=(conn, address, num))
        client_handler.start()


# 处理收发数据
def handle_client(conn, address, num):
    while True:
        # 接收客户端发来的数据
        data_from_client: str = conn.recv(1024).decode("UTF-8")
        print(f"客户端 {num}号:{address}发来的消息是：{data_from_client}")
        # 发送消息到客户端
        msg = input(f"请输入你要回复客户端 {num}号:{address}的消息：")
        if msg == 'exit':
            break
        conn.send(msg.encode("UTF-8"))  # encode将字符串编码为字节数组对象
    conn.close()


if __name__ == '__main__':
    server_host = input("请输入服务端Host:")
    server_port = int(input("请输入服务端port:"))
    create_server_socket(server_host, server_port)