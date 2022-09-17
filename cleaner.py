import psutil
import shutil
import os
def killServers():
    for ps in psutil.process_iter(['name']):
        if ps.info['name']=='staff_server.exe':
            print(ps.info)
            # ps.kill()

def cleanCache():
    path=os.path.expandvars('%TEMP%\\staff-cache')
    for cache in os.listdir(path):
        shutil.rmtree(path+'\\'+cache)

if __name__ == '__main__':
    killServers()
    # cleanCache()