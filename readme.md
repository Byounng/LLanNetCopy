## 局域网文件多线程传送脚本
此脚本用于局域网或是多层级网络设备间文件互传 ，
- 可以用在双设备可以相互PING通，此时双方谁做客户端谁做服务端无所谓
- 也可与用在高层级网络可以单向PING通低层级网络， 比如 A 设备IP 在学校内网IP是 10.84.2.188（设备A） 而你要传送给的设备在这个层级的子网下，其IP是192.168.0.66 (设备B) ，那么此时只有B可以PING到A，这种情况拿A做服务端，B做客户端,B连接到A ，然后双方可以相互发送文件。

####  requirement: tqdm 

### NOTE:
- -path 参数可以用来指定单个文件或文件夹。如果指定的是文件夹，该文件夹下只能包含文件，不能有子文件夹。例如，-path a.pth 是有效的，-path c:\\file_wait_trs 也是有效的，但前提是文件夹 c:\\file_wait_trs 下没有子文件夹。

- 保存端路径： ` .\received_files `



### CLI.py

参数修改：



作为服务端（接收文件）：
`python cli.py -mode server`


作为客户端（发送文件）：
`python cli.py -mode client -action send -ip 192.168.0.1 -path your_path`


作为客户端（接收文件）：
`python cli.py -mode client -ip 192.168.0.1`


作为服务端（发送文件）：
`python cli.py -mode server -action send -path your_path`




