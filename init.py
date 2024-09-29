# configuration module

import socket

nb=1 # 0- HIT-"139.162.222.115", 1 - open HiveMQ - broker.hivemq.com
brokers=[str(socket.gethostbyname('vmm1.saaintertrade.com')), str(socket.gethostbyname('broker.hivemq.com')),"18 .194.176.210"]
ports=['80','1883','1883']
usernames = ['','',''] # should be modified for HIT
passwords = ['','',''] # should be modified for HIT
broker_ip=brokers[nb]
port=ports[nb]
username = usernames[nb]
password = passwords[nb]
conn_time = 0 # 0 stands for endless
# mzs=['matzi/','']
# sub_topics =[mzs[nb]+'#','#']
# pub_topics = [mzs[nb]+'test', 'test']
# ext_man = mzs[nb]+'system/command'
# sub_topic = [mzs[nb]+'bearer/accel/status', mzs[nb]+'bearer/belt/status']
# pub_topic = mzs[nb]+'system/state'
msg_system = ['normal', 'issue','No issue']
wait_time = 5

broker_ip=brokers[nb]
broker_port=ports[nb]
username = usernames[nb]
password = passwords[nb]
# sub_topic = sub_topics[nb]
# pub_topic = pub_topics[nb]

# Common
conn_time = 0 # 0 stands for endless loop
comm_topic = 'pr/PetMonitoring/'
#comm_topic = 'pr/Smart/Home/'


# FFT module init data
isplot = False
issave = False

# DSP init data
percen_thr=0.05 # 5% of max energy holds
Fs = 2048.0
deviation_percentage = 10
max_eucl = 0.5 

# Acq init data
acqtime = 60.0 # sec
manag_time = 10 # sec

# DB init data 
db_name = 'data\\petData_05_2.db' # SQLite
db_init =  False   #False # True if we need reinit smart home setup

# Meters consuption limits"
Water_max=2.2
Food_max=1.8