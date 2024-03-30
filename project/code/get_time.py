import ntplib
from datetime import datetime

# 创建 NTPClient 对象
ntp_client = ntplib.NTPClient()
# 选择 NTP 服务器
ntp_server = 'pool.ntp.org' # 
ntp_server_2 = 'ntp1.aliyun.com' # 备用ntp

def get_now_time():
    global ntp_client, ntp_server

    ntp_time = datetime.now() # 获取当前本地时间

    # 尝试获取联网时间
    try:
        response = ntp_client.request(ntp_server, version=3) # 获取联网时间1
        ntp_time = datetime.fromtimestamp(response.tx_time) 
    except:
        print("ERROR when get response 1") #
        try: 
            response = ntp_client.request(ntp_server_2, version=3) # 获取联网时间2
            ntp_time = datetime.fromtimestamp(response.tx_time) 
        except:
            print("ERROR when get response 2") #

    return ntp_time

#
# print("get_now_time() =", get_now_time()) # 
    


    