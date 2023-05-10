import argparse
import os
from auxiliary.logs import logger
from core.ip_scan import ip_parse, is_reachable
from core.os_detect import os_scan
from core.nmap_port_scan import nmap_port_service_scan
from core.nmap_port_scan import Nmap_Portscan


def parse_start(opt):
    if opt.ip:
    # TODO: 后续支持指定端口段扫描
    # if not opt.p: 
    #     logger.log("ERROR","please input the port range you want to scan,like -p 1-65535 ")
    # else:
        Nmap_Portscan(opt.ip)
        exit(1)
    if not opt.skip_ip_find:
        ip_list = ip_parse(opt.ip_range)
        port_list = opt.p
        if os.path.exists('ip_collect.txt'):
            os.remove('ip_collect.txt')
        if os.path.exists('ip_os_collect.txt'):
            os.remove('ip_os_collect.txt')
   
        is_reachable(ip_list)
    if os.path.exists('port_service.txt'):
        os.remove('port_service.txt')
    if opt.os :
        os_scan()
    if opt.p:
        nmap_port_service_scan(opt.p)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip_range", type=str,
                        help='input ip_range: 192.168.5.1-100')
    parser.add_argument("--ip", type=str,
                        help='input ip: 192.168.5.1')
    parser.add_argument("-p", type=str,
                        help='input port_range: 80-81')
    parser.add_argument("--os", help='scan os type', action='store_true')
    parser.add_argument("--skip_ip_find", help='use old ip_collect.txt if set skip_ip_find', action='store_true')
    opt = parser.parse_args()
    if opt.ip_range == None and opt.ip == None:
        logger.log("ALERT", f'请输入目标,帮助使用-h查看')
    else:
        parse_start(opt)
    