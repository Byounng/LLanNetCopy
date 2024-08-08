import socket
import os
import tqdm
import time

########################NOTE########################
'''
You only need to modify here
'''
IS_SERVER = False  # 是否作为服务器运行
IS_SEND = True    # 是否发送文件
Opposite_IP = '127.0.0.1'  # 对方的IP地址
FILE_PATHS = [r"E:\newwwww\trs_ts"]  # 要发送的目录路径或文件路径
########################NOTE########################


def get_file_paths(directory):
    """Get all file paths from the specified directory."""
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

if IS_SERVER:
    FLAG = 'DST'
    LISTEN_IP = '0.0.0.0'  # 监听的IP地址
else:
    FLAG = 'FROM'
    DST_IP = Opposite_IP  # 目标IP地址（接收端）

if IS_SEND:
    SED_REC = 'S'
    if FILE_PATHS is None:
        raise ValueError("File paths must be provided when sending files.")
    # If a directory is provided, get all files in the directory
    if len(FILE_PATHS) == 1 and os.path.isdir(FILE_PATHS[0]):
        FILE_PATHS = get_file_paths(FILE_PATHS[0])
else:
    SED_REC = 'R'

BUFFER_SIZE = 4096
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # 获取脚本所在目录
SAVE_DIR = os.path.join(SCRIPT_DIR, 'received_files')  # 保存接收文件的目录
LISTEN_PORT = 5000  # 监听端口号
EOF_FLAG = False
def create_socket():
    """创建套接字。"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s

def connect_socket(s, ip, port):
    """连接到指定IP和端口的套接字。"""
    s.connect((ip, port))
    print(f"[+] Connected to {ip}:{port}")

def bind_socket(s, ip, port):
    """绑定套接字到指定IP和端口并监听。"""
    s.bind((ip, port))
    s.listen(5)
    print(f"[+] Server started, listening on {ip}:{port}")

def send_file(s, file_path):
    """发送文件到连接的套接字。"""
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    print(f"[+] Preparing to send file:")
    print(f"    File path: {file_path}")
    print(f"    File size: {file_size / (1024 * 1024):.2f} MB")
    
    # 发送文件信息（以UTF-8编码）
    file_info = f"{file_name}:{file_size}".encode('utf-8')
    file_info_header = f"{len(file_info):<10}".encode('utf-8')
    s.send(file_info_header + file_info)
    
    start_time = time.time()  # 记录传输开始时间
    
    # 创建进度条
    with open(file_path, 'rb') as f:
        progress_bar = tqdm.tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024, desc=f"Sending {file_name}")
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)
            progress_bar.update(len(bytes_read))
    
    end_time = time.time()  # 记录传输结束时间
    progress_bar.close()
    
    # 计算传输时间和速率
    transfer_time = end_time - start_time
    transfer_rate = (file_size / (1024 * 1024)) / transfer_time  # MB/s
    
    print(f"[+] File {file_name} sent")
    print(f"[+] Transfer time: {transfer_time:.2f} seconds")
    print(f"[+] Transfer rate: {transfer_rate:.2f} MB/s  \n")

def receive_file(s):
    """从连接的套接字接收文件。"""

    try:
        file_info_header = s.recv(10).decode('utf-8').strip()
        file_info_size = int(file_info_header)
        file_info = s.recv(file_info_size).decode('utf-8')
        file_name, file_size = file_info.split(':')
        if file_name == 'end':
            print('[-] All files received')
            global EOF_FLAG
            EOF_FLAG = True
            return
        file_size = int(file_size)
    except Exception as e:
        print(f"[-] Error receiving file information: {e}")
        return
    PRINT_SAVE_DIR = os.path.join(SAVE_DIR, file_name)
    print(f"[+] Preparing to receive file:")
    print(f"    File name: {file_name}")
    print(f"    File size: {file_size / (1024 * 1024):.2f} MB")
    print(f"    Save path: {SAVE_DIR}")  
    print(f"    Save location: {PRINT_SAVE_DIR}  ")
    
    start_time = time.time()  # 记录接收开始时间
    
    # 创建保存目录（如果不存在）
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    
    # 创建进度条
    with open(os.path.join(SAVE_DIR, file_name), 'wb') as f:
        progress_bar = tqdm.tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024, desc=f"Receiving {file_name}")
        received = 0
        while received < file_size:
            bytes_read = s.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            received += len(bytes_read)
            progress_bar.update(len(bytes_read))
    
    end_time = time.time()  # 记录接收结束时间
    progress_bar.close()
    
    # 计算传输时间和速率
    transfer_time = end_time - start_time
    transfer_rate = (file_size / (1024 * 1024)) / transfer_time  # MB/s
    
    print(f"[+] File {file_name} received")
    print(f"[+] Transfer time: {transfer_time:.2f} seconds")
    print(f"[+] Transfer rate: {transfer_rate:.2f} MB/s\n")


def main():
    if FLAG == 'FROM':   #kehuduan
        if SED_REC == 'S':
            for file_path in FILE_PATHS:
                s = create_socket()
                connect_socket(s, DST_IP, LISTEN_PORT)
                send_file(s, file_path)
                s.close()
        #发送结束标志
            s = create_socket()
            connect_socket(s, DST_IP, LISTEN_PORT)
            file_info = f"end:-1".encode('utf-8')
            file_info_header = f"{len(file_info):<10}".encode('utf-8')
            s.send(file_info_header + file_info)
            s.close()
            print('[-] All files sent')
        elif SED_REC == 'R':
            while True:
                s = create_socket()
                connect_socket(s, DST_IP, LISTEN_PORT)
                receive_file(s)
                if EOF_FLAG == True:
                    return
                s.close()   

    elif FLAG == 'DST':   #fuwuduan
        if SED_REC == 'R':
            s = create_socket()
            bind_socket(s, LISTEN_IP, LISTEN_PORT)
            while True:

                conn, addr = s.accept()
                print(f"[+] Connection from {addr}")
                receive_file(conn)
                conn.close()
                if EOF_FLAG == True:
                    s.close()
                    return 
        elif SED_REC == 'S':
            for file_path in FILE_PATHS:
                s = create_socket()
                bind_socket(s, LISTEN_IP, LISTEN_PORT)
                client_socket, client_address  = s.accept()
                # print("服务端发送开始log")
                print(f"[+] Connection from {client_address}")
                
                send_file(client_socket, file_path)
                client_socket.close()
            
            #发送结束标志
            s = create_socket()
            bind_socket(s, LISTEN_IP, LISTEN_PORT)
            client_socket, client_address  = s.accept()
            file_info = f"end:-1".encode('utf-8')
            file_info_header = f"{len(file_info):<10}".encode('utf-8')
            client_socket.send(file_info_header + file_info)
            print('[-] All files sent')
            client_socket.close()
            s.close()


if __name__ == "__main__":
    main()
