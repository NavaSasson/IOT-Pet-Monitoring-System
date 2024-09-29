import os
from sqlite3.dbapi2 import Date
import sys
import random
# pip install pyqt5-tools
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.pyplot import get
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
from init import *
from init import comm_topic
from agent import Mqtt_client 
import time
from icecream import ic
from datetime import datetime 
import data_acq as da
# pip install pyqtgraph
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import paho.mqtt.client as mqtt

import logging
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = 'C:/Users/נאוה ששון/AppData/Local/Programs/Python/Python38/Lib/site-packages/PyQt5/Qt5/plugins'
# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
file_handler = logging.FileHandler('logfile_gui.log')
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

global petDataReceived
petDataReceived = True

# def time_format():
#     return f'{datetime.now()}  GUI|> '

def time_format():
    return f'{datetime.now()}  GUI|> '
ic.configureOutput(prefix=time_format)
ic.configureOutput(includeContext=False) # use True for including script file context file 
# Creating Client name - should be unique 
global clientname
r=random.randrange(1,10000) # for creating unique client ID
clientname="IOT_clientId-nXLMZeDcjH"+str(r)

def check(fnk):    
    try:
        rz=fnk
    except:
        rz='NA'
    return rz 
class MC(Mqtt_client):
    def __init__(self):
        super().__init__()
    # def __init__(self):
    #     # broker IP adress:
    #     self.broker=''
    #     self.topic=''
    #     self.port='' 
    #     self.clientname=''
    #     self.username=''
    #     self.password=''        
    #     self.subscribeTopic=''
    #     self.publishTopic=''
    #     self.publishMessage=''
        self.on_connected_to_form = ''
        
    # Setters and getters
    def set_on_connected_to_form(self,on_connected_to_form):
        self.on_connected_to_form = on_connected_to_form
    def get_broker(self):
        return self.broker
    def set_broker(self,value):
        self.broker= value         
    def get_port(self):
        return self.port
    def set_port(self,value):
        self.port= value     
    def get_clientName(self):
        return self.clientName
    def set_clientName(self,value):
        self.clientName= value        
    def get_username(self):
        return self.username
    def set_username(self,value):
        self.username= value     
    def get_password(self):
        return self.password
    def set_password(self,value):
        self.password= value         
    def get_subscribeTopic(self):
        return self.subscribeTopic
    def set_subscribeTopic(self,value):
        self.subscribeTopic= value        
    def get_publishTopic(self):
        return self.publishTopic
    def set_publishTopic(self,value):
        self.publishTopic= value         
    def get_publishMessage(self):
        return self.publishMessage
    def set_publishMessage(self,value):
        self.publishMessage= value 
        
        
    def on_log(self, client, userdata, level, buf):
        print("log: "+buf)
            
    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            print("connected OK")
            self.on_connected_to_form();            
        else:
            print("Bad connection Returned code=",rc)
            
    def on_disconnect(self, client, userdata, flags, rc=0):
        print("DisConnected result code "+str(rc))
            
    # def on_message(self, client, userdata, msg):
    #     topic=msg.topic
    #     m_decode=str(msg.payload.decode("utf-8","ignore"))
    #     print("message from:"+topic, m_decode)
    #     mainwin.subscribeDock.update_mess_win(m_decode)

    def on_message(self, client, userdata, msg):
        global petDataReceived
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        ic(f"Message from: {topic}, {m_decode}")
        mainwin.subscribeDock.update_mess_win(m_decode)

        # Check the topic and update the corresponding fields in StatusDock
        if 'Food' in m_decode:
            food_level = m_decode.split('Food: ')[1]  # Extract food level data
            mainwin.statusDock.update_food_level(food_level)
            if food_level == 'Low':
                mainwin.graphsDock.update_food_meter('0.3')
            elif food_level == 'Full':
                mainwin.graphsDock.update_food_meter('1.8')
            else:
                mainwin.graphsDock.update_food_meter('0.0')

        elif 'Water' in m_decode:
            water_level = m_decode.split('Water: ')[1]  # Extract water level data
            mainwin.statusDock.update_water_level(water_level)
            if water_level == 'Low':
                mainwin.graphsDock.update_Water_meter('0.2')
            elif water_level == 'Full':
                mainwin.graphsDock.update_Water_meter('2.2')
            else:
                mainwin.graphsDock.update_Water_meter('0.0')

        elif 'Temp' in m_decode:
            temp_level = m_decode.split('Temperature: ')[1]  # Extract temperature data
            mainwin.statusDock.update_temp_level(temp_level)
            mainwin.airconditionDock.update_temp_Room(temp_level)

        elif 'Act' in m_decode:
            activity_level = m_decode.split('Activity: ')[1]  # Extract activity level data
            mainwin.statusDock.update_act_level(activity_level)

        petDataReceived = not petDataReceived  # Toggle to handle multiple updates


    def connect_to(self):
        # Init paho mqtt client class        
        self.client = mqtt.Client(self.clientname, clean_session=True) # create new client instance        
        self.client.on_connect=self.on_connect  #bind call back function
        self.client.on_disconnect=self.on_disconnect
        self.client.on_log=self.on_log
        self.client.on_message=self.on_message
        self.client.username_pw_set(self.username,self.password)        
        print("Connecting to broker ",self.broker)        
        self.client.connect(self.broker,self.port)     #connect to broker
    
    def disconnect_from(self):
        self.client.disconnect()                   
    
    def start_listening(self):        
        self.client.loop_start()        
    
    def stop_listening(self):        
        self.client.loop_stop()    
    
    def subscribe_to(self, topic):        
        self.client.subscribe(topic)
              
    def publish_to(self, topic, message):
        self.client.publish(topic,message)   

# class MC(Mqtt_client):
#     def __init__(self):
#         super().__init__()

#     def on_message(self, client, userdata, msg):
#         global petsDataReceived
#         topic = msg.topic
#         m_decode = str(msg.payload.decode("utf-8", "ignore"))
#         ic("message from:"+topic, m_decode)
#         if 'PetsData' in topic:
#             if petsDataReceived:
#                 mainwin.graphsDock.update_food_level(check(m_decode.split('FoodLevel: ')[1].split(' WaterLevel: ')[0]))
#                 petsDataReceived = False
#             else:
#                 mainwin.graphsDock.update_water_level(check(m_decode.split(' WaterLevel: ')[1]))
#                 petsDataReceived = True

class ConnectionDock(QDockWidget):
    """Connection settings for the pet monitoring system."""
    def __init__(self, mc):
        super().__init__()
        self.mc = mc
        self.topic = comm_topic+'#' 
        self.mc.set_on_connected_to_form(self.on_connected)   
        self.eHostInput = QLineEdit()
        self.eHostInput.setText('broker.hivemq.com')        
        self.ePort = QLineEdit()
        self.ePort.setMaxLength(4)
        self.ePort.setText('1883')        
        self.eClientID = QLineEdit()
        # self.eClientID.setText("PetMonitoringClient")
        global clientname
        self.eClientID.setText(clientname) 
        self.eConnectButton = QPushButton("Connect", self)
        self.eConnectButton.clicked.connect(self.on_button_connect_click)
        self.eConnectButton.setStyleSheet("background-color: red")
        formLayout = QFormLayout()
        formLayout.addRow("Host", self.eHostInput)
        formLayout.addRow("Port", self.ePort)
        formLayout.addRow("", self.eConnectButton)
        widget = QWidget(self)
        widget.setLayout(formLayout)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)     
        self.setWindowTitle("Connect") 
    
    def on_connected(self):
        self.eConnectButton.setStyleSheet("background-color: green")
        self.eConnectButton.setText('Connected')

    def on_button_connect_click(self):
        self.mc.set_broker(self.eHostInput.text())
        self.mc.set_port(int(self.ePort.text()))
        self.mc.set_clientName(self.eClientID.text())
        self.mc.connect_to()        
        self.mc.start_listening()
        time.sleep(1)
        if not self.mc.subscribed:
            self.mc.subscribe_to(self.topic)

class PublishDock(QDockWidget):
    """Publisher """

    def __init__(self,mc):
        QDockWidget.__init__(self)
        
        self.mc = mc        
                
        self.ePublisherTopic=QLineEdit()
        self.ePublisherTopic.setText(comm_topic+'Home/pub')

        self.eQOS=QComboBox()
        self.eQOS.addItems(["0","1","2"])

        self.eMessageBox=QPlainTextEdit()        
        self.ePublishButton = QPushButton("Publish",self)
        
        formLayot=QFormLayout()        
        formLayot.addRow("Topic",self.ePublisherTopic)
        formLayot.addRow("QOS",self.eQOS)
        formLayot.addRow("Message",self.eMessageBox)
        formLayot.addRow("",self.ePublishButton)
        
        self.ePublishButton.clicked.connect(self.on_button_publish_click)
        
        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setWidget(widget) 
        self.setWindowTitle("Publish")         
       
    def on_button_publish_click(self):
        self.mc.publish_to(self.ePublisherTopic.text(), self.eMessageBox.toPlainText())
        self.ePublishButton.setStyleSheet("background-color: yellow")

class SubscribeDock(QDockWidget):
    """Subscribe """

    def __init__(self,mc):
        QDockWidget.__init__(self)        
        self.mc = mc
        
        self.eSubscribeTopic=QLineEdit()
        self.eSubscribeTopic.setText(comm_topic+'#') 
        
        self.eQOS = QComboBox()
        self.eQOS.addItems(["0","1","2"])
        
        self.eRecMess=QTextEdit()

        self.eSubscribeButton = QPushButton("Subscribe",self)
        self.eSubscribeButton.clicked.connect(self.on_button_subscribe_click)

        formLayot=QFormLayout()       
        formLayot.addRow("Topic",self.eSubscribeTopic)
        formLayot.addRow("QOS",self.eQOS)
        formLayot.addRow("Received",self.eRecMess)
        formLayot.addRow("",self.eSubscribeButton)
                
        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setWidget(widget)
        self.setWindowTitle("Subscribe")
        
    def on_button_subscribe_click(self):
        print(self.eSubscribeTopic.text())
        self.mc.subscribe_to(self.eSubscribeTopic.text())
        self.eSubscribeButton.setStyleSheet("background-color: yellow")
    
    # create function that update text in received message window
    def update_mess_win(self,text):
        #self.eRecMess.append(text)
        self.eRecMess.append(text)

class StatusDock(QDockWidget):
    """Status display for pet information."""
    def __init__(self, mc):
        super().__init__()
        self.mc = mc
        self.eFoodLevelLabel = QLineEdit()
        self.eWaterLevelLabel = QLineEdit()
        self.eTempLevelLabel = QLineEdit()
        self.eActLevelLabel = QLineEdit()
        formLayout = QFormLayout()
        formLayout.addRow("Food Level:", self.eFoodLevelLabel)
        formLayout.addRow("Water Level:", self.eWaterLevelLabel)
        formLayout.addRow("Room Temperature:", self.eTempLevelLabel)
        formLayout.addRow("Activity:", self.eActLevelLabel)
        widget = QWidget(self)
        widget.setLayout(formLayout)
        self.setWidget(widget)
        self.setWindowTitle("Status")

    def update_food_level(self, text):
        self.eFoodLevelLabel.setText(text)

    def update_water_level(self, text):
        self.eWaterLevelLabel.setText(text)

    def update_temp_level(self, text):
        self.eTempLevelLabel.setText(text)

    def update_act_level(self, text):
        self.eActLevelLabel.setText(text)

# class GraphsDock(QDockWidget):
#     """Graphs for pet data visualization."""
#     def __init__(self, mc):
#         super().__init__()
#         self.mc = mc        
#         self.eStartDate = QLineEdit()
#         self.eEndDate = QLineEdit()
#         self.eDateButton = QPushButton("Load Data", self)
#         self.eDateButton.clicked.connect(self.on_button_date_click)
#         formLayout = QFormLayout()
#         formLayout.addRow("Start Date:", self.eStartDate)
#         formLayout.addRow("End Date:", self.eEndDate)
#         formLayout.addRow("", self.eDateButton)
#         widget = QWidget(self)
#         widget.setLayout(formLayout)
#         self.setWidget(widget)
#         self.setWindowTitle("Graphs")
        

#     def on_button_date_click(self):
#         start_date = self.eStartDate.text()
#         end_date = self.eEndDate.text()
#         self.update_plot(start_date, end_date)

#     def update_plot(self, start_date, end_date):
#         results = da.filter_by_date('data', start_date, end_date, 'Feeding')
#         timestamps = []
#         food_levels = []
#         for row in results:
#             timestamps.append(row[2])  # Assuming timestamp is in the 2nd index
#             food_levels.append(float(row[3]))  # Assuming food level is in the 3rd index
#         mainwin.plotsDock.plot(timestamps, food_levels)

# class PlotDock(QDockWidget):
#     """Plotting dock for pets data."""
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Plots")
#         self.graphWidget = pg.PlotWidget()
#         self.setWidget(self.graphWidget)

#     def plot(self, timestamps, food_levels):
#         self.graphWidget.clear()
#         self.graphWidget.plot(timestamps, food_levels, pen='r')  # Example pen color
class GraphsDock(QDockWidget):
    """Graphs """
    def __init__(self,mc):
        QDockWidget.__init__(self)        
        self.mc = mc        
        self.eFoodButton = QPushButton("Show",self)
        self.eFoodButton.clicked.connect(self.on_button_Food_click)        
        self.eFoodText=QLineEdit()
        self.eFoodText.setText(" ")
        self.eWaterButton = QPushButton("Show",self)
        self.eWaterButton.clicked.connect(self.on_button_Water_click)
        self.eWaterText= QLineEdit()
        self.eWaterText.setText(" ")
        self.eStartDate= QLineEdit()
        self.eEndDate= QLineEdit()
        self.eStartDate.setText("2021-05-10")
        self.eEndDate.setText("2021-05-25")
        self.eDateButton=QPushButton("Insert", self)
        self.eDateButton.clicked.connect(self.on_button_date_click)
        self.date=self.on_button_date_click
        formLayot=QFormLayout()       
        formLayot.addRow("Food meter",self.eFoodButton)
        formLayot.addRow(" ", self.eFoodText)
        formLayot.addRow("Water meter",self.eWaterButton)
        formLayot.addRow(" ", self.eWaterText)
        formLayot.addRow("Start date: ", self.eStartDate)
        formLayot.addRow("End date: ", self.eEndDate)
        formLayot.addRow("", self.eDateButton)
        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setWidget(widget)
        self.setWindowTitle("Graphs")

    def update_Water_meter(self, text):
        self.eWaterText.setText(text)

    def update_food_meter(self, text):
        self.eFoodText.setText(text) 

    def on_button_date_click (self):
        self.stratDateStr= self.eStartDate.text()
        self.endDateStr= self.eEndDate.text()        

    def on_button_Water_click(self):
       self.update_plot(self.stratDateStr, self.endDateStr, 'SmartWater')
       self.eWaterButton.setStyleSheet("background-color: yellow")

    def on_button_Food_click(self):
        self.update_plot(self.stratDateStr, self.endDateStr, 'SmartFeeder')
        self.eFoodButton.setStyleSheet("background-color: yellow")

    def update_plot(self,date_st,date_end, meter):
        rez= da.filter_by_date('data',date_st,date_end, meter)
        temperature = []  
        timenow = []       
        for row in rez:
            timenow.append(row[1])
            temperature.append(float("{:.2f}".format(float(row[2]))))
        print(timenow)
        print(temperature)
        mainwin.plotsDock.plot(timenow, temperature) 


class AirconditionDock(QDockWidget):
    """Aircondition """
    def __init__(self,mc):
        QDockWidget.__init__(self)        
        self.mc = mc
        # Line #1
        self.l1 = QLabel()
        self.l1.setText("Air conditioner remote settings:")
        self.l1.setFont(QFont('Arial', 10))
        self.l1.setStyleSheet("color: rgb(0, 0, 255);")
        # self.l1.setAlignment(Qt.AlignCenter)
        self.cb = QComboBox()        
        self.cb.addItems(["Living Room", "Kitchen", "Bedroom"])
        self.cb.currentIndexChanged.connect(self.selectionchange)
		# Line #2
        self.l21 = QLabel()
        self.l21.setText("Temperature: ")
        self.cRoomTemp=QLineEdit()
        self.cRoomTemp.setText(" ")
        self.l22 = QLabel()
        self.cRoomTemp.textChanged.connect(self.cr_textchange)  
        self.l22.setText("Target")        
        self.tRoomTemp = QComboBox()        
        self.tRoomTemp.addItems(["16c", "17c", "18c", "19c", "20c", "21c", "22c", "23c", "24c", "25c", "26c", "27c", "28c", "29c", "30c"])
        self.tRoomTemp.currentIndexChanged.connect(self.tr_selectionchange)    
        self.settemp='16c'
        self.topic_sub = comm_topic+'#'
        self.topic_pub = comm_topic+'Home/pub'

        # Line #3
        self.l31 = QLabel()
        self.l31.setText("Mode")
        self.md = QComboBox()        
        self.md.addItems(["Cool", "Heat", "Dry","Fan"])
        self.md.currentIndexChanged.connect(self.md_selectionchange)
        self.l32 = QLabel()
        self.l32.setText("Fan")
        self.fn = QComboBox()        
        self.fn.addItems(["High", "Middle", "Low"])
        self.fn.currentIndexChanged.connect(self.fn_selectionchange)
        # Line #4
        self.l41 = QLabel()
        self.l41.setText("ON\OFF:")
        self.od = QComboBox()        
        self.od.addItems(["ON", "OFF"])        
        self.od.currentIndexChanged.connect(self.od_selectionchange)
        self.l42 = QLabel()
        self.l42.setText("Status:")
        # self.st = QComboBox()        
        # self.st.addItems(["Unknown", "Failure", "Normal"])
        # self.st.currentIndexChanged.connect(self.st_selectionchange)
        # Line #5
        self.setButton = QPushButton("SET(UPDATE)",self)
        self.setButton.clicked.connect(self.on_setButton_click)
        layout = QGridLayout()
        # Add widgets to the layout
        # Line #1
        layout.addWidget(self.l1, 0,1)
        layout.addWidget(self.cb, 0,2)
        # Line #2 
        layout.addWidget(self.l21, 1,0)
        layout.addWidget(self.cRoomTemp, 1,1)
        layout.addWidget(self.l22, 1,2)
        layout.addWidget(self.tRoomTemp, 1,3)
        # Line #3 
        layout.addWidget(self.l31, 2,0)
        layout.addWidget(self.md, 2,1)
        layout.addWidget(self.l32, 2,2)
        layout.addWidget(self.fn, 2,3)
        # Line #4 
        layout.addWidget(self.l41, 3,0)
        layout.addWidget(self.od, 3,1)
        layout.addWidget(self.l42, 3,2)
        # layout.addWidget(self.st, 3,3)
        # Line #5 
        layout.addWidget(self.setButton, 4,1,4,2)       
        # Set the layout on the application's window
        # self.setLayout(layout)
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setWidget(widget)
        self.setWindowTitle("Aircondition Temperature")

    def update_temp_Room(self, text):
        self.cRoomTemp.setText(text)  

    def selectionchange(self,i):
        print ("Current index",i,"selection changed ",self.cb.currentText())

    def md_selectionchange(self,i):
        print ("Current index",i,"selection changed ",self.md.currentText())

    def fn_selectionchange(self,i):
        print ("Current index",i,"selection changed ",self.fn.currentText())

    def od_selectionchange(self,i):
        print ("Current index",i,"selection changed ",self.od.currentText())
        if "ON" in self.od.currentText():
            self.od.setStyleSheet("color: green")
        elif "OFF" in self.od.currentText():
            self.od.setStyleSheet("color: red")

        #setStyleSheet("color: blue;"
        #                "background-color: yellow;"
        #                "selection-color: yellow;"
        #                "selection-background-color: blue;");    

    # def st_selectionchange(self,i):
    #     print ("Current index",i,"selection changed ",self.st.currentText())  

    def tr_selectionchange(self,i):
        print ("Current index",i,"selection changed ",self.tRoomTemp.currentText())  
        self.cRoomTemp.setText(self.tRoomTemp.currentText())
        self.mc.publish_to(self.topic_pub,'Temperature: '+ self.settemp)
    
    def cr_textchange(self,i):
        print ("Current index",i,"selection changed ",self.cRoomTemp.text())  
        self.settemp=self.cRoomTemp.text()

    def on_setButton_click(self):
        self.setButton.setStyleSheet("background-color: green")             
        self.mc.publish_to(self.topic_pub,'Temperature: '+ self.settemp)
        

class PlotDock(QDockWidget):
    """Plots """
    def __init__(self):
        QDockWidget.__init__(self)        
        self.setWindowTitle("Plots")
        self.graphWidget = pg.PlotWidget()
        self.setWidget(self.graphWidget)
        rez= da.filter_by_date('pet_data.db','2021-05-16','2021-05-18', 'SmartFeeder')        
        datal = []  
        timel = []   
     
        for row in rez:
            timel.append(row[1])
            datal.append(float("{:.2f}".format(float(row[2]))))
        self.graphWidget.setBackground('b')
        # Add Title
        self.graphWidget.setTitle("Consuption Timeline", color="w", size="15pt")
        # Add Axis Labels
        styles = {"color": "#f00", "font-size": "20px"}
        self.graphWidget.setLabel("left", "Value (°C/m3)", **styles)
        self.graphWidget.setLabel("bottom", "Date (dd.hh/hh.mm)", **styles)
        #Add legend
        self.graphWidget.addLegend()
        #Add grid
        self.graphWidget.showGrid(x=True, y=True)
        #Set Range
        #self.graphWidget.setXRange(0, 10, padding=0)
        #self.graphWidget.setYRange(20, 55, padding=0)            
        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line=self.graphWidget.plot( datal,  pen=pen)

    def plot(self, timel, datal):
        self.data_line.setData( datal)  # Update the data.

class MainWindow(QMainWindow):    
    def __init__(self):
        super().__init__()
        self.mc = MC()        
        self.setGeometry(30, 100, 1200, 600)
        self.setWindowTitle('Pet Monitoring System')
        self.connectionDock = ConnectionDock(self.mc)        
        self.statusDock = StatusDock(self.mc)
        self.graphsDock = GraphsDock(self.mc)
        self.plotsDock = PlotDock()
        self.graphsDock = GraphsDock(self.mc)
        self.airconditionDock= AirconditionDock(self.mc)
        self.publishDock =   PublishDock(self.mc)
        self.subscribeDock = SubscribeDock(self.mc)
        self.addDockWidget(Qt.TopDockWidgetArea, self.connectionDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.statusDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.graphsDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.plotsDock)     
        self.addDockWidget(Qt.TopDockWidgetArea, self.airconditionDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.publishDock)  
        self.addDockWidget(Qt.BottomDockWidgetArea, self.subscribeDock)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwin = MainWindow()
    mainwin.show()
    app.exec_()
