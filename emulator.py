import sys
import os
import random
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from init import *
from init import broker_ip, port, username, password, comm_topic
from agent import Mqtt_client
from icecream import ic
from datetime import datetime

import logging
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = 'C:/Users/נאוה ששון/AppData/Local/Programs/Python/Python38/Lib/site-packages/PyQt5/Qt5/plugins'

# Setup Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logfile_emulator.log')
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Time formatter for icecream debugging
def time_format():
    return f'{datetime.now()}  Emulator|> '

ic.configureOutput(prefix=time_format)
ic.configureOutput(includeContext=False)

# Creating Client name - should be unique
global clientname, tmp_upd
r = random.randrange(1, 10000000)
clientname = "PetMonitor-Id-" + str(r)

# MQTT Client class
class MC(Mqtt_client):
    def __init__(self):
        super().__init__()

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        ic(f"message from: {topic}", m_decode)
        self.message_received.emit(m_decode)  # Emit the message
        try:
            mainwin.connectionDock.update_btn_state(m_decode)
        except Exception as e:
            ic(f"Error updating button state: {e}")
    

# Connection Dock class for UI
class ConnectionDock(QDockWidget):
    def __init__(self, mc, name, topic_sub, topic_pub):
        QDockWidget.__init__(self)
        self.name = name
        self.topic_sub = topic_sub
        self.topic_pub = topic_pub
        self.mc = mc
        self.mc.set_on_connected_to_form(self.on_connected)
        self.setup_ui()

    def setup_ui(self):
        self.eHostInput = QLineEdit()
        self.eHostInput.setInputMask('999.999.999.999')
        self.eHostInput.setText(broker_ip)
        self.ePort = QLineEdit()
        self.ePort.setValidator(QIntValidator())
        self.ePort.setMaxLength(4)
        self.ePort.setText(port)
        self.eClientID = QLineEdit()
        global clientname
        self.eClientID.setText(clientname)
        self.eUserName = QLineEdit()
        self.eUserName.setText(username)
        self.ePassword = QLineEdit()
        self.ePassword.setEchoMode(QLineEdit.Password)
        self.ePassword.setText(password)
        self.eKeepAlive = QLineEdit()
        self.eKeepAlive.setValidator(QIntValidator())
        self.eKeepAlive.setText("60")
        self.eSSL = QCheckBox()
        self.eCleanSession = QCheckBox()
        self.eCleanSession.setChecked(True)
        self.eConnectbtn = QPushButton("Enable/Connect", self)
        self.eConnectbtn.clicked.connect(self.on_button_connect_click)
        self.eConnectbtn.setStyleSheet("background-color: gray")

        # Dynamic UI layout based on pet type
        self.PetStatus = QLineEdit()
        self.PetStatus.setText('')

        formLayout = QFormLayout()
        if 'Feed' in self.name:
            self.ePublisherTopic = QLineEdit()
            self.ePublisherTopic.setText(self.topic_pub)
            self.FoodLevel = QLineEdit()
            self.FoodLevel.setText('')
            formLayout.addRow("Turn On/Off", self.eConnectbtn)
            formLayout.addRow("Sub topic", self.ePublisherTopic)
            formLayout.addRow("Food Level", self.FoodLevel)
        elif 'Water' in self.name:
            self.ePublisherTopic = QLineEdit()
            self.ePublisherTopic.setText(self.topic_pub)
            self.WaterLevel = QLineEdit()
            self.WaterLevel.setText('')
            formLayout.addRow("Turn On/Off", self.eConnectbtn)
            formLayout.addRow("Pub topic", self.ePublisherTopic)
            formLayout.addRow("Water Level", self.WaterLevel)
        elif 'Temp' in self.name:
            self.ePublisherTopic = QLineEdit()
            self.ePublisherTopic.setText(self.topic_pub)
            self.ePushtbtn = QPushButton("", self)
            self.ePushtbtn.setToolTip("Push me")
            self.ePushtbtn.setStyleSheet("background-color: gray")
            self.Temperature = QLineEdit()
            self.Temperature.setText('')
            self.WaterLevel = QLineEdit()
            self.WaterLevel.setText('')
            formLayout.addRow("Turn On/Off", self.eConnectbtn)
            formLayout.addRow("Pub topic", self.ePublisherTopic)
            formLayout.addRow("Status", self.ePushtbtn)
            formLayout.addRow("Temperature:", self.Temperature)
            formLayout.addRow("Water Level", self.WaterLevel)
        elif 'Act' in self.name:
            self.ePublisherTopic = QLineEdit()
            self.ePublisherTopic.setText(self.topic_pub)
            self.ePushtbtn = QPushButton("", self)
            self.ePushtbtn.setToolTip("Push me")
            self.ePushtbtn.setStyleSheet("background-color: gray")
            self.Activity = QLineEdit()
            self.Activity.setText('')
            self.FoodLevel = QLineEdit()
            self.FoodLevel.setText('')
            formLayout.addRow("Turn On/Off", self.eConnectbtn)
            formLayout.addRow("Pub topic", self.ePublisherTopic)
            formLayout.addRow("Status", self.ePushtbtn)
            formLayout.addRow("Activity:", self.Activity)
            formLayout.addRow("Food Level", self.FoodLevel)
        else:
            self.ePublisherTopic = QLineEdit()
            self.ePublisherTopic.setText(self.topic_pub)
            self.FoodLevel = QLineEdit()
            self.FoodLevel.setText('')
            self.WaterLevel = QLineEdit()
            self.WaterLevel.setText('')
            formLayout.addRow("Turn On/Off", self.eConnectbtn)
            formLayout.addRow("Pub topic", self.ePublisherTopic)
            formLayout.addRow("Food Level", self.FoodLevel)
            formLayout.addRow("Water Level", self.WaterLevel)

        widget = QWidget(self)
        widget.setLayout(formLayout)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)
        self.setWindowTitle("Pet Monitoring Emulator")

    def on_connected(self):
        self.eConnectbtn.setStyleSheet("background-color: green")

    def push_button_click(self):
        self.mc.publish_to(self.ePublisherTopic.text(), '"value":1')
    
    def on_button_connect_click(self):
        self.mc.set_broker(self.eHostInput.text())
        self.mc.set_port(int(self.ePort.text()))
        self.mc.set_clientName(self.eClientID.text())
        self.mc.set_username(self.eUserName.text())
        self.mc.set_password(self.ePassword.text())
        self.mc.connect_to()
        self.mc.start_listening()

    def update_btn_state(self, messg):
        global tmp_upd
        if 'Set' in messg:
            try:
                tmp = messg.split('Set status to: ')[1]
                self.PetStatus.setText(tmp)
                self.ePushtbtn.setStyleSheet("background-color: green")
            except:
                ic("Error parsing pet status!")
            tmp_upd = tmp

# Main Window class
class MainWindow(QMainWindow):
    def __init__(self, args, parent=None):
        QMainWindow.__init__(self, parent)
        global tmp_upd
        self.name = args[1]
        print(args[1])
        self.units = args[2]
        self.topic_sub = comm_topic + args[3] + '/sub'
        self.topic_pub = comm_topic + args[3] + '/pub'
        self.update_rate = args[4]
        self.mc = MC()
        self.timer = QtCore.QTimer(self)

        # Configure updates based on pet type
        if 'Feed' in self.name:
            tmp_upd = 'Full'
            self.timer.timeout.connect(self.create_feed_data)
        elif 'Water' in self.name:
            tmp_upd = 'Full'
            self.timer.timeout.connect(self.create_water_data)
        elif 'Act' in self.name:
            tmp_upd = 'Playing'
            self.timer.timeout.connect(self.create_activity_data)
        elif 'Temp' in self.name:
            tmp_upd = '25c'
            self.timer.timeout.connect(self.create_temperature_data)
        else:
            tmp_upd = 'Low'
            self.timer.timeout.connect(self.create_general_data)

        self.timer.start(int(self.update_rate) * 1000)
        # general GUI settings
        self.setUnifiedTitleAndToolBarOnMac(True)
        # set up main window
        self.setGeometry(30, 600, 300, 150)
        self.setWindowTitle(self.name)
        # Init QDockWidget objects        
        self.connectionDock = ConnectionDock(self.mc, self.name, self.topic_sub, self.topic_pub)       
        self.addDockWidget(Qt.TopDockWidgetArea, self.connectionDock)    

    def create_feed_data(self):
        global tmp_upd
        current_status = random.choice(['Full', 'Low', 'Empty'])
        self.connectionDock.FoodLevel.setText(current_status)
        if not self.mc.connected:
            self.connectionDock.on_button_connect_click()
        self.mc.publish_to(self.topic_pub,f'Food: {current_status}')
    
    def create_water_data(self):
        global tmp_upd
        current_status = random.choice(['Full', 'Low', 'Empty'])
        self.connectionDock.WaterLevel.setText(current_status)
        if not self.mc.connected:
            self.connectionDock.on_button_connect_click()
        self.mc.publish_to(self.topic_pub,f'Water: {current_status}')

    def create_activity_data(self):
        global tmp_upd
        current_status_act = random.choice(['Climbing', 'Sleeping', 'Eating', 'Hunting', 'Playing'])
        current_status_feed = random.choice(['Full', 'Low', 'Empty'])
        self.connectionDock.Activity.setText(current_status_act)
        self.connectionDock.FoodLevel.setText(current_status_feed)
        if not self.mc.connected:
            self.connectionDock.on_button_connect_click()
        self.mc.publish_to(self.topic_pub, f'Activity: {current_status_act}')
        self.mc.publish_to(self.topic_pub, f'Food: {current_status_feed}')
    
    def create_temperature_data(self):
        global tmp_upd
        current_status_temp = random.choice(['16c', '17c', '18c', '19c', '20c', '21c', '22c', '23c', '24c', '25c', '26c', '27c', '28c', '29c', '30c'])
        current_status_water = random.choice(['Full', 'Low', 'Empty'])
        self.connectionDock.Temperature.setText(current_status_temp)
        self.connectionDock.WaterLevel.setText(current_status_water)
        if not self.mc.connected:
            self.connectionDock.on_button_connect_click()
        self.mc.publish_to(self.topic_pub, f'Temperature: {current_status_temp}')
        self.mc.publish_to(self.topic_pub, f'Water: {current_status_water}')


    def create_general_data(self):
        global tmp_upd
        food_level = random.choice(['Full', 'Low', 'Empty'])
        water_level = random.choice(['Full', 'Low', 'Empty'])
        self.connectionDock.FoodLevel.setText(food_level)
        self.connectionDock.WaterLevel.setText(water_level)
        if not self.mc.connected:
            self.connectionDock.on_button_connect_click()
        self.mc.publish_to(self.topic_pub, f'Food: {food_level}, Water: {water_level}')

# Main application runner
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        argv = sys.argv
        if len(argv) == 1:
            argv.append('Cat')
            argv.append('pet-1')
            argv.append('7')

        mainwin = MainWindow(argv)
        mainwin.show()
        app.exec_()
    except Exception as e:
        logger.exception(f"Crash: {e}")
