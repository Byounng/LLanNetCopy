## 局域网文件多线程传送脚本

- trs_cli.py
- trs.py

### trs.py

参数修改：

Eng:

```
  You only need to modify here
  IS_SERVER = False  # Whether to run as a server, if not, you need to provide the IP address of the other party

  IS_SEND = False  # Whether to send files

  Opposite_IP = '10.85.236.249'

  FILE_PATHS = [r"F:\YY\SING_TRACK\new_EfficenetNetv2M.pth"]  # The path of the file to be sent
```

中文：

```
  你只需要更改这里

  IS_SERVER = False  # 是否作为服务器运行,是则先运行,  如果是否  则需要提供对方的IP地址

  IS_SEND = False  # 是否发送文件

  Opposite_IP = IP   #作为服务端时可以不填写

  FILE_PATHS = [r"F:\YY\SING_TRACK\new_EfficenetNetv2M.pth"]  # 要发送的文件路径
```

### trs_CLI.py

参数修改：

```
  作为服务端（接收文件）
  python name.py -srv
  作为客户端（发送文件）
  python name.py -ip 192.168.0.1 -sed -fs path/to/file1 path/to/file2
  作为客户端（接收文件）
  python name.py -ip 192.168.0.1
  作为服务端（发送文件）
  python name.py -srv -sed -fs path/to/file1 path/to/file2


  作为客户端（发送文件）的详细命令行参数解析：
  python name.py -ip <SERVER_IP> -sed -fs <FILE_PATH1> <FILE_PATH2> ...
  作为服务端（接收文件）的详细命令行参数解析：
  python name.py -srv
  作为客户端（接收文件）的详细命令行参数解析：
  python name.py -ip <SERVER_IP>
  作为服务端（发送文件）的详细命令行参数解析：
  python name.py -srv -sed -fs <FILE_PATH1> <FILE_PATH2> ...
```
