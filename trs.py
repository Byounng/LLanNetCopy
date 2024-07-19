import socket
import os
import tqdm
import time


########################NOTE########################
'''
You only need to modify here
IS_SERVER = False  # Whether to run as a server, if not, you need to provide the IP address of the other party
IS_SEND = False  # Whether to send files
Opposite_IP = '10.85.236.249'
FILE_PATHS = [r"F:\YY\SING_TRACK\new_EfficenetNetv2M.pth"]  # The path of the file to be sent
你只需要更改这里
IS_SERVER = False  # 是否作为服务器运行,是则先运行,  如果是否  则需要提供对方的IP地址
IS_SEND = False  # 是否发送文件
Opposite_IP = '
FILE_PATHS = [r"F:\YY\SING_TRACK\new_EfficenetNetv2M.pth"]  # 要发送的文件路径

'''
IS_SERVER = False  # Whether to run as a server, if not, you need to provide the IP address of the other party
IS_SEND = False  # Whether to send files
Opposite_IP = '10.85.236.249'
FILE_PATHS = [r"F:\YY\SING_TRACK\new_EfficenetNetv2M.pth"]  # The path of the file to be sent
########################NOTE########################

if IS_SERVER:
    FLAG = 'DST'
    LISTEN_IP = '0.0.0.0'  # Listening IP address
else:
    FLAG = 'FROM'
    DST_IP = Opposite_IP  # Target IP address (receiver)

if IS_SEND:
    SED_REC = 'S'
    FILE_PATHS = FILE_PATHS  # The path of the file to be sent
else:
    SED_REC = 'R'

BUFFER_SIZE = 4096
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory where the script is located
SAVE_DIR = os.path.join(SCRIPT_DIR, 'received_files')  # Directory to save received files
LISTEN_PORT = 5000  # Listening port number

def create_socket():
    """Create a socket."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s

def connect_socket(s, ip, port):
    """Connect to the socket at the specified IP and port."""
    s.connect((ip, port))
    print(f"[+] Connected to {ip}:{port}")

def bind_socket(s, ip, port):
    """Bind the socket to the specified IP and port and listen."""
    s.bind((ip, port))
    s.listen(5)
    print(f"[+] Server started, listening on {ip}:{port}")

def send_file(s, file_path):
    """Send a file to the connected socket."""
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    print(f"[+] Preparing to send file:")
    print(f"    File path: {file_path}")
    print(f"    File size: {file_size / (1024 * 1024):.2f} MB")
    
    # Send file information (encoded in UTF-8)
    file_info = f"{file_name}:{file_size}".encode('utf-8')
    s.send(file_info)
    
    start_time = time.time()  # Record the start time of the transfer
    
    # Create a progress bar
    with open(file_path, 'rb') as f:
        progress_bar = tqdm.tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024, desc=f"Sending {file_name}")
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)
            progress_bar.update(len(bytes_read))
    
    end_time = time.time()  # Record the end time of the transfer
    progress_bar.close()
    
    # Calculate transfer time and rate
    transfer_time = end_time - start_time
    transfer_rate = (file_size / (1024 * 1024)) / transfer_time  # MB/s
    
    print(f"[+] File {file_name} sent")
    print(f"[+] Transfer time: {transfer_time:.2f} seconds")
    print(f"[+] Transfer rate: {transfer_rate:.2f} MB/s")

def receive_file(s):
    """Receive a file from the connected socket."""
    try:
        file_info = s.recv(BUFFER_SIZE).decode('utf-8')
        file_name, file_size = file_info.split(':')
        file_size = int(file_size)
    except Exception as e:
        print(f"[-] Error receiving file information: {e}")
        return
    PRINT_SAVE_DIR = os.path.join(SAVE_DIR, file_name)
    print(f"[+] Preparing to receive file:")
    print(f"    File name: {file_name}")
    print(f"    File size: {file_size / (1024 * 1024):.2f} MB")
    print(f"    Save path: {SAVE_DIR}")  
    print(f"    Save location: {PRINT_SAVE_DIR}")
    
    start_time = time.time()  # Record the start time of the reception
    
    # Create the save directory (if it does not exist)
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    
    # Create a progress bar
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
    
    end_time = time.time()  # Record the end time of the reception
    progress_bar.close()
    
    # Calculate transfer time and rate
    transfer_time = end_time - start_time
    transfer_rate = (file_size / (1024 * 1024)) / transfer_time  # MB/s
    
    print(f"[+] File {file_name} received")
    print(f"[+] Transfer time: {transfer_time:.2f} seconds")
    print(f"[+] Transfer rate: {transfer_rate:.2f} MB/s")

def handle_client(client_socket, addr):
    """Handle client connection, receive and send files."""
    print(f"[+] Connection from {addr}")
    if SED_REC in ('R', 'r'):
        receive_file(client_socket)
    elif SED_REC in ('S', 's'):
        for file_path in FILE_PATHS:
            send_file(client_socket, file_path)
    client_socket.close()

def start_server():
    """Start the server and listen for client connections."""
    server_socket = create_socket()
    bind_socket(server_socket, LISTEN_IP, LISTEN_PORT)
    
    while True:
        client_socket, addr = server_socket.accept()
        handle_client(client_socket, addr)

def main():
    s = create_socket()
    if FLAG == 'FROM':
        connect_socket(s, DST_IP, LISTEN_PORT)
    elif FLAG == 'DST':
        bind_socket(s, LISTEN_IP, LISTEN_PORT)
        s, addr = s.accept()
        print(f"[+] Connection from {addr}")

    if SED_REC in ('S', 's'):
        for file_path in FILE_PATHS:
            send_file(s, file_path)
    elif SED_REC in ('R', 'r'):
        receive_file(s)
    
    s.close()

if __name__ == "__main__":
    main()
