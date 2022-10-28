import copy
from lib.config import ALL_OS
from auxiliary.logs import logger
from multiprocessing.dummy import Pool as ThreadPool
from lib.method import test_os_using_icmp,test_os_using_tcp,smb_scan_os

def os_scan():
    pool = ThreadPool()
    ip_list = []
    with open('port_collect.txt','r') as f:
        iplist = f.readlines()
        ip_list = [(ip.strip().split(" ")[0],ip.strip().split(" ")[1]) for ip in iplist]
        # for ip in iplist:
        #     ip_list.append(ip.strip().split(" ")[0])
    pool.map(os_scan_ip,ip_list)

def os_scan_ip(ip_tuple:tuple):
    
    verbose = True
    result_set = copy.deepcopy(ALL_OS)
    logger.log("INFOR","开始使用Ping检测操作系统类型")
    icmp_os_set = test_os_using_icmp(ip_tuple[0], verbose=verbose)
    result_set.intersection_update(icmp_os_set)
    logger.log("INFOR",f"Ping检测结果为：{'、'.join(result_set)}")

    if len(result_set) > 2:
        logger.log("INFOR","开始使用TCP端口检测操作系统类型")
        tcp_os_set = test_os_using_tcp(dst_ip=ip_tuple[0], verbose=verbose)
        if len(tcp_os_set) > 0:
            result_set.intersection_update(tcp_os_set)
            logger.log("INFOR",f"TCP检测结果为：{'、'.join(result_set)}")

    for o in result_set:
        if "win" in o.lower():
            try:
                logger.log("INFOR","开始使用SMB端口检测操作系统类型")
                result = smb_scan_os(ip_tuple[0], timeout=5)
                if result:
                    result_set = [result]
                    logger.log("INFOR",f"SMB检测结果为：{result_set}")
                break
            except:
                break

    if len(result_set) == 1:
        result_set = list(result_set)[0]
    elif len(result_set) > 1:
        for o in result_set:
            if "win" in o.lower():
                result_set = "Windows"
                break
        else:
            result_set = "Linux"
    else:
        result_set = "Windows"

    logger.log("INFOR",f"操作系统最终检测结果为：{result_set}")
    with open("port_os_colletct.txt",'a') as f:
        f.write(ip_tuple[0]+" " +ip_tuple[1]+" "+result_set + "\n")
    return result_set