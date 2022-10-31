import subprocess
import os
from multiprocessing.dummy import Pool as ThreadPool

from auxiliary.logs import logger

def ip_parse(ip_range:str) -> list:
    '''解析ip
        Args:
            ip_range: str ex:192.168.1.1-100
        Return:
            
    '''
    if '-' not in ip_range:
        return [ip_range]
    ip_list = []
    head = ip_range.split("-")[0].split('.')[-1]
    tail = ip_range.split('-')[-1]
    body = ".".join(ip_range.split("-")[0].split('.')[0:3])
    for num in range(int(head),int(tail)+1):
        ip_list.append(body+'.'+str(num))
    return ip_list




def is_reachable(ip_list:list):
    '''判断ip是否可达
    '''
    pool = ThreadPool()
    pool.map(Ping,ip_list)
  

def Ping(ip_or_domain):
    p = subprocess.Popen('ping '+ip_or_domain +' -c 1 -W 4', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = p.communicate()
    
    with open('ip_collect.txt','a') as f:
        if stderr != b'':
            if b'Name or service not known\n' in stderr:
                #logger.log('ERROR',f'{stderr}')
                print(False,'未知域名/服务',ip_or_domain)
            elif b'Temporary failure in name resolution\n' in stderr:
                #logger.log('ERROR',f'{stderr}')
                print(False,'域名解析失败',ip_or_domain)
            else:
                #logger.log('ERROR',f'{stderr}')
                print(False,'未知异常',ip_or_domain)

        if b'100% packet loss' in stdout : 
            if b'Destination Host Unreachable' in stdout:
                #logger.log('ERROR',f'{ip_or_domain} Destination Host Unreachable')
                print(False,'连接异常',ip_or_domain)
            else:
                stdout = str(stdout).split('\\n')[0].split(' ')[1]
                if '.'.join(ip_or_domain.split('.')[1:]) != stdout and ip_or_domain != stdout:
                    #logger.log('INFOR',f'存在cdn或云防，{stdout}')
                    print(True,stdout,ip_or_domain)
                    f.write(ip_or_domain+" ×ping" +"\n")
                else:
                    #logger.log('INFOR',f'未检测到cdn或云防,{stdout}')
                    print(True,'暂无',ip_or_domain)
                    f.write(ip_or_domain+" ×ping" +"\n")
        else:
            stdout = str(stdout).split('\\n')[0].split(' ')[1]
            if '.'.join(ip_or_domain.split('.')[1:]) != stdout and ip_or_domain != stdout:
                #logger.log('INFOR',f'存在cdn或云防，{stdout}')
                print(True,stdout,ip_or_domain)
                f.write(ip_or_domain+" √ping" +"\n")
            else:
                #logger.log('INFOR',f'未检测到cdn或云防,{stdout}')
                print(True,'暂无',ip_or_domain)
                f.write(ip_or_domain+" √ping" +"\n")


