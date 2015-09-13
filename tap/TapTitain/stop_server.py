import subprocess
from config import Configration

__author__ = 'Mike'
class StopServer:
    @staticmethod
    def stopSerer():
        port = Configration.port
        cmd = "netstat -anp | awk '$1==\"tcp\"&&$4 ~ /:%s/{print $7}' | awk -F\/ '{print $NF}' | xargs killall -9"%port
        subprocess.Popen(cmd)
        print("server stoped :%s" %port)

StopServer.stopSerer()