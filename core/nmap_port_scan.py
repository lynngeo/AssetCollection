import subprocess
import copy
#/usr/bin/nmap -sV -p80 192.168.1.1

cmd = ["usr/bin/nmap","-sV","-p"]

def nmap_port_service_scan(port):
    with open('ip_collect.txt','r') as f:
        iplist = f.readlines()
        valid_ip = [ip.strip().split(" ")[0] for ip in iplist]
    
    cmd = ["/usr/bin/nmap","-sV","-p"]
    cmd.append(port)
    newcmd = copy.copy(cmd)
   
    
    for ip in valid_ip:
        with open("port_service.txt","a") as f:
            newcmd.append(ip)
            p = subprocess.Popen(newcmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout,_ = p.communicate()
            f.write(stdout.decode("utf-8")+"\n")
        newcmd = copy.copy(cmd)

    
