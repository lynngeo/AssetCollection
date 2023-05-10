import subprocess
import copy
import nmap
import socket
from auxiliary.logs import logger
from concurrent.futures import ThreadPoolExecutor, as_completed
from lib.config import nmap_search_path
#/usr/bin/nmap -sV -p80 192.168.1.1

cmd = ["usr/bin/nmap","-sV","-p"]

def nmap_port_service_scan(port):
    with open('ip_collect.txt','r') as f:
        iplist = f.readlines()
        valid_ip = [ip.strip().split(" ")[0] for ip in iplist]
    
    cmd = [nmap_search_path,"-sV","-p"]
    cmd.append(port)
    newcmd = copy.copy(cmd)
   
    
    for ip in valid_ip:
        with open("port_service.txt","a") as f:
            newcmd.append(ip)
            p = subprocess.Popen(newcmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout,_ = p.communicate()
            f.write(stdout.decode("utf-8")+"\n")
        newcmd = copy.copy(cmd)

def Nmap_Portscan(ip):  # Nmap扫描
    try:
        port_dict = {}
        logger.log('INFOR', f'nmap[{ip}]开始扫描')
        if ip.split('.')[-1] == "255" or ip.split(".")[-1] == "0":  #nmap扫描.0或.255结尾的ip无法结束，过滤掉
            return
        try:
            nm = nmap.PortScanner(nmap_search_path=nmap_search_path)
        except Exception as e:
            logger.log('ERROR', f'nmap程序未找到:{e}')
            return None
        
        multi_port_list = Multi_Openport_scan(ip,"detect")
        #nm.scan(hosts=ip, arguments='-Pn -T 4 -sV --version-intensity=3 -p 1-10')
        open_port_num = len(multi_port_list)


        # 如果显示所有10个端口都扫到，可能是由于路由器做了处理（我们内网做了处理导致所以端口都通...)
        if open_port_num == 10:
            logger.log('ALERT', f'被测ip{ip}可能存在防止端口扫描的机制')
            return "FORBIDDEN"
        else:
            multi_port_list = Multi_Openport_scan(ip,"all")
            print(multi_port_list)
            ports = ",".join(multi_port_list)
            nm.scan(hosts=ip, arguments=f'-Pn -T 4 -sV --version-intensity=3 -p {ports}')
        # -sV:打开版本探测；-T 4:Aggressive模式假设用户具有合适及可靠的网络从而加速扫描; -Pn/-P0：将所有指定的主机视作开启的，跳过主机发现的过程
        # –version-intensity<intensity>：设置版本扫描强度，范围为0-9，默认是7，强度越高，时间越长，服务越可能被正确识别
        try:
            port_list = nm[ip]['tcp'].keys()  # 查看扫描的端口哪些端口提供了TCP协议, 只返还端口,返回列表型数据
        except Exception as e:
            logger.log('ERROR', f'nmap扫描端口异常{e}')
            return None
        else:
            
            for port in port_list:
                if nm[ip].has_tcp(port):  # 判断该端口是否提供TCP协议
                    port_info = nm[ip]['tcp'][port]
                    # port_info的示例：
                    # {445:
                        # {'product': 'Microsoft Windows 7 - 10 microsoft-ds',
                        # 'state': 'open',
                        # 'version': '',
                        # 'name': 'microsoft-ds',
                        # 'conf': '10',
                        # 'extrainfo': 'workgroup: WORKGROUP',
                        # 'reason': 'syn-ack',
                        # 'cpe': 'cpe:/o:microsoft:windows'}
                    # }
                    state = port_info.get('state', 'no')  # 查看该协议下端口的状态
                    reason = port_info.get('reason', 'no')
                    if state == 'open':
                        name = port_info.get('name', '')
                        product = port_info.get('product', '')
                        version = port_info.get('version', '')
                        port_dict[port] = {'ip': ip, 'port': port, 'name': name, 'product': product, 'version': version}
                        logger.log('INFOR', f'nmap扫描:{ip}:{port} {name} {product} {version}')
                    elif state == 'filtered' and reason == 'no-response':
                        name = port_info.get('name', '')
                        product = port_info.get('product', '')
                        version = port_info.get('version', '')
                        port_dict[port] = {'ip': ip, 'port': port, 'name': name, 'product': product, 'version': version}
                        logger.log('INFOR', f'nmap扫描:{ip}:{port} {name} {product} {version}')
        logger.log('INFOR', f'nmap[{ip}]扫描完成')
    except Exception as e:
        logger.log("ERROR",f'错误{e}')
    return port_dict


def Multi_Openport_scan(ip,mode) -> list:
    '''
        多线程快速扫描开放端口
        Args:
            ip:str 待测ip
            mode:detect(仅检测1-10端口)
                 all(检测所有端口)

        Return:
            port_list:list 开放的端口列表
    '''
    port_list = []
    def async_add(ip,port):
        try:
            s = socket.create_connection((ip, port), timeout=1)
            port_list.append(str(port))
        except ConnectionRefusedError:
            pass
        except socket.error:
            logger.log("ALERT",f'超时{ip}:{port}')
        except Exception:
            pass
        finally:
            s.shutdown(socket.SHUT_RDWR)
            s.close()

    pool = ThreadPoolExecutor(max_workers=500,thread_name_prefix='PORT_SCAN')
    all_task = []
    if mode == "detect": 
        all_task = [pool.submit(async_add, ip, port) for port in range(1,11)]
    elif mode == "all":
        all_task = [pool.submit(async_add, ip, port) for port in range(1,65536)]
    else:
        logger.log('ERROR',"未知模式")
    for _ in as_completed(all_task):
        pass
        
    pool.shutdown()  
    return port_list
    
