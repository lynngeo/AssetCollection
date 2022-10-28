import argparse
import os
from auxiliary.logs import logger
from core.ip_scan import ip_parse, is_reachable
from core.os_detect import os_scan


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip_range", type=str,
                        help='input ip_range: 192.168.5.1-100')
    parser.add_argument("--os", help='scan os type', action='store_true')
    opt = parser.parse_args()
    if opt.ip_range == None:
        logger.log("ALERT", f'请输入目标,帮助使用-h查看')
    ip_list = ip_parse(opt.ip_range)
    if os.path.exists('port_collect.txt'):
        os.remove('port_collect.txt')
    if os.path.exists('port_os_collect.txt'):
        os.remove('port_os_collect.txt')
    is_reachable(ip_list)
    if opt.os :
        os_scan()
