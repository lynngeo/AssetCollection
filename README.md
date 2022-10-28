由于使用nmap扫描开放ip和系统版本时速度非常慢
所以研发此工具用于扫描开放ip段及系统版本，高并发零误报

```
python3 main.py -h
usage: main.py [-h] [--ip_range IP_RANGE] [--os]

optional arguments:
  -h, --help           show this help message and exit
  --ip_range IP_RANGE  input ip_range: 192.168.5.1-100
  --os                 scan os type
```

# 仅扫描ip段
python3 main.py --ip_range 192.168.5.1-100

结果位于port_collect.txt中，结果示例
```
192.168.1.1 √ping
192.168.1.21 √ping
192.168.1.49 √ping
192.168.1.61 √ping
192.168.1.22 √ping
192.168.1.25 √ping
192.168.1.26 √ping
192.168.1.17 √ping
192.168.1.29 √ping
192.168.1.30 √ping
192.168.1.5 ×ping
192.168.1.9 ×ping
```

# 扫描ip段和扫描系统版本
python3 main.py --ip_range 192.168.5.1-100

结果位于port_os_collect.txt中，结果示例

```
192.168.1.30 √ping Linux
192.168.1.49 √ping Linux
192.168.1.1 √ping Linux
192.168.1.59 √ping Windows 10.0 Build 19041
192.168.1.54 √ping Windows 10.0 Build 22000
192.168.1.77 √ping Linux
192.168.1.8 √ping Linux
192.168.1.25 √ping Linux
192.168.1.29 √ping Linux
192.168.1.47 √ping Linux
192.168.1.70 ×ping Windows
192.168.1.67 ×ping Linux
192.168.1.10 √ping Linux
192.168.1.26 √ping Linux
192.168.1.21 √ping Linux
192.168.1.61 √ping Windows 10.0 Build 19041
192.168.1.48 ×ping Windows
192.168.1.33 ×ping Windows
192.168.1.16 ×ping Windows
```