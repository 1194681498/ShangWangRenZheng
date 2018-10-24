#coding=utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore, QtGui, QtWidgets
#爬虫库
from urllib import request,parse
from http import cookiejar
import threading
#工具库
import sys
import re
from subprocess import check_output
import json
import os
import win32con
import win32api
import random
import subprocess
import time


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!


class Ui_widget(object):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(455, 279)
        self.verticalLayout = QtWidgets.QVBoxLayout(widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(widget)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.student_number = QtWidgets.QLineEdit(widget)
        self.student_number.setMinimumSize(QtCore.QSize(0, 35))
        self.student_number.setInputMask("")
        self.student_number.setText("")
        self.student_number.setObjectName("student_number")
        self.horizontalLayout_3.addWidget(self.student_number)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.password = QtWidgets.QLineEdit(widget)
        self.password.setEnabled(True)
        self.password.setMinimumSize(QtCore.QSize(0, 35))
        self.password.setInputMask("")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.horizontalLayout_2.addWidget(self.password)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.rmb_password = QtWidgets.QCheckBox(widget)
        self.rmb_password.setEnabled(True)
        self.rmb_password.setCheckable(True)
        self.rmb_password.setChecked(True)
        self.rmb_password.setObjectName("rmb_password")
        self.horizontalLayout.addWidget(self.rmb_password)
        self.powerBoot = QtWidgets.QCheckBox(widget)
        self.powerBoot.setChecked(True)
        self.powerBoot.setObjectName("powerBoot")
        self.horizontalLayout.addWidget(self.powerBoot)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.btn_send = QtWidgets.QPushButton(widget)
        self.btn_send.setEnabled(True)
        self.btn_send.setObjectName("btn_send")
        self.verticalLayout.addWidget(self.btn_send)
        self.display_info = QtWidgets.QTextBrowser(widget)
        self.display_info.setObjectName("display_info")
        self.verticalLayout.addWidget(self.display_info)

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "Form"))
        self.label.setText(_translate("widget", "学号："))
        self.student_number.setPlaceholderText(_translate("widget", "请输入学号"))
        self.label_2.setText(_translate("widget", "密码："))
        self.password.setPlaceholderText(_translate("widget", "请输入密码"))
        self.rmb_password.setText(_translate("widget", "记住用户名和密码"))
        self.powerBoot.setText(_translate("widget", "开机自启+自动登陆"))
        self.btn_send.setText(_translate("widget", "认证"))

class Mythread(QThread):
    #定义显示信号
    breakSignal = pyqtSignal(str,bool)
    #定义登陆信号
    loginSignal=pyqtSignal()
    def __init__(self,parent=None,UI=None):
        super().__init__(parent)
        self.loginUI =UI
        # 下面的初始化方法都可以，有的python版本不支持
        #  super(Mythread, self).__init__()
        self.IS_WIN32 = 'win32' in str(sys.platform).lower()

    def run(self):
        """
                功能：检查当前WIFI是否符合要求
                :return:
                """
        self.breakSignal.emit('正在获取WIFI信息......',False)
        while True:
            # 执行命令，获取当前的WLAN信息
            p=subprocess.Popen('netsh WLAN show interfaces',stdout=subprocess.PIPE)
            # p = self.subprocess_call("netsh WLAN show interfaces", stdout=subprocess.PIPE)
            # p = commands.getstatusoutput("ls")
            p.wait()  # 等待执行命令结束
            # 如果捕获到异常，则证明当前用户没有连接到WIFI，那么程序不会再往下执行！
            try:
                result_lines = p.stdout.readlines()  # 获取执行后的输出结果
                WIFIList = result_lines[-4].decode('gbk')  # 获取存放Wifi的那列结果
                # print(WIFIList)
                # 以冒号作为分割，提取里面的WIFI名称
                currentSSID = WIFIList[WIFIList.index(':') + 1:].strip()
                self.breakSignal.emit('当前wifi为：%s' % currentSSID,False)
                # 检查是否链接到指定的Wifi
                if not (str(currentSSID) == "GFXY_5G" or currentSSID == "GFXY"):
                    self.breakSignal.emit('请链接Wifi到“GFXY_5G”或“GFXY”后再试！', True)
                    self.loginUI.setEnabled(False)
                    # self.breakSignal.emit('程序将在3秒钟之后自动退出', True)
                    # self.closeWindowTimer.start()
                else:
                    self.breakSignal.emit('WIFI信息符合要求,请您继续操作',False)
                    self.loginUI.setEnabled(True)
                    self.loginSignal.emit()
                    break
            except ValueError as e:
                self.breakSignal.emit('未检测到wifi！', True)
                self.loginUI.setEnabled(False)
            time.sleep(1)


class loginUI(QWidget):
    loginSignal=pyqtSignal(str,str)
    def __init__(self):
        super(loginUI, self).__init__()
        # 构建一个关闭窗口的定时器
        # 定时器构造函数主要有2个参数，第一个参数为时间，第二个参数为函数名
        self.closeWindowTimer = threading.Timer(3, self.closeWindow)  # 3秒调用一次函数
        # 引入用Qt designer构建的程序
        self.ui = Ui_widget()
        self.ui.setupUi(self)
        # 读取配置文件
        self.configDict = self.readConfig()
        if self.configDict==None:
            self.configDict={"student_number": "", "password": "", "rmb_password": False, "powerBoot": False}
        # 关联登陆按钮
        self.ui.btn_send.clicked.connect(self.login)
        self.ui.powerBoot.clicked.connect(self.changePowerBoot)
    def changeRmb(self):
        """
        功能：根据用户是否选择记住密码，而修改配置信息
        :return:
        """
        rmb_password = self.ui.rmb_password
        if rmb_password.isChecked():
            # 已经被勾选,设置为False
            #print('记住密码')
            #学号
            student_number=self.ui.student_number.text()
            #密码
            password=self.ui.password.text()
            if student_number == "" or password == "":
                self.displayInfo('账号或密码不能为空', True)
                return
            #记录当前用户选择状态，方便下次读取
            self.configDict["rmb_password"] = True
            #记录当前用户学号
            self.configDict["student_number"]=student_number
            #记录当前用户密码
            self.configDict["password"]=password
        else:
            # 没有被勾选
            #print('取消记住密码')
            self.configDict["rmb_password"] = False
            self.configDict["student_number"]=""
            self.configDict["password"]=""

        # 写入配置信息
        self.writeConfig()
    def changePowerBoot(self):
        """
        功能：根据用户是否选择开机自启而，修改配置文件
        :return:
        """
        power_boot=self.ui.powerBoot
        if power_boot.isChecked():
            #print('开机自启')
            self.configDict["powerBoot"]=True
            #添加开机启动
            self.addPowerBoot(os.getcwd()+"\\"+__file__[:-2]+"exe")
        else:
            #print('取消开机自启')
            self.configDict["powerBoot"]=False
            #删除开机启动
            self.delPowerBoot("")
        self.writeConfig()
            # rmb_password.setChecked(False)
    def readConfig(self):
        fileName=os.path.join(getExePath(),"configuration.json")
        # 读取配置文件
        if os.path.exists(fileName):
            #根据配置文件修改界面信息
            #记住密码
            config=json.load(open(fileName,'r'))
            rmb_password= True if config["rmb_password"] else False
            self.ui.rmb_password.setChecked(rmb_password)
            #如果用户勾选了记住密码，那么在启动程序时，自动加载账号密码
            if rmb_password:
                self.ui.student_number.setText(config["student_number"])
                self.ui.password.setText(config["password"])
            # 开机自启
            power_boot = True if config["powerBoot"] else False
            self.ui.powerBoot.setChecked(power_boot)
            return config
        else:
            return None
    def writeConfig(self):
        """
            功能：将当前配置信息写入到文件
        :return:
        """
        #确认文件路径
        pwd=os.path.join(getExePath(),"configuration.json")
        json.dump(self.configDict, open(pwd, "w", encoding="utf-8"), ensure_ascii=False)
    # 修改注册表以达到开机自动启动
    def addPowerBoot(self,path):
        #print('开机启动')
        "注册到启动项"
        runpath = "Software\Microsoft\Windows\CurrentVersion\Run"
        hKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, runpath, 0, win32con.KEY_SET_VALUE)
        (filepath, filename) = os.path.split(path)
        win32api.RegSetValueEx(hKey, "WindowsInit", 0, win32con.REG_SZ, path)
        win32api.RegCloseKey(hKey)
        #print(path)
    def delPowerBoot(self,path):
        runpath = "Software\Microsoft\Windows\CurrentVersion\Run"
        hKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, runpath, 0, win32con.KEY_SET_VALUE)
        (filepath, filename) = os.path.split(path)
        win32api.RegSetValueEx(hKey, "WindowsInit", 0, win32con.REG_SZ, path)
        win32api.RegCloseKey(hKey)
    def autoLogin(self):
        fileName=os.path.join(getExePath(),"configuration.json")
        print(fileName)
        if os.path.exists(fileName):
            config=json.load(open(fileName,'r'))
            result=True if config["powerBoot"] else False
            if result:
                self.displayInfo('正在进行自动登陆……',False)
                self.login()
    def login(self):
        """
        功能：开始上网认证
        :return:
        """
        #如果读取到配置信息
        # if self.configDict:
        #检查是否需要记住密码
        self.changeRmb()
        #检查是否需要开启启动
        self.changePowerBoot()
        # 学号
        student_number = self.ui.student_number.text()
        # 密码
        password = self.ui.password.text()
        if student_number == "" or password == "":
            self.displayInfo('账号或密码不能为空',True)
            return
        # self.infoDialog.show()

        # infoThread=threading.Thread(target=self.infoDialog.exec_)
        # infoThread.start()
        # infoDialog.closeSignal.connect(self.closeInfoDialog)
        # infoThread.pushButton.clicked.connect(self.closeInfoDialog)

        # displayThread=threading.Thread(target=self.displayDialog)
        # displayThread.start()
        # 用户名
        student_num = widget.ui.student_number.text()
        # 密码
        password = widget.ui.password.text()
        self.loginSignal.emit(student_num,password)
    def closeWindow(self):
        # 定时器触发后，则关闭窗口
        QCoreApplication.instance().quit()
    #添加背景图片
    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     pixmap = QPixmap("backgroundImage.jpg")
    #     painter.drawPixmap(self.rect(), pixmap)
    def keyPressEvent(self, QKeyEvent):
        """
        功能：监听回车键，调用登陆函数
        :param QKeyEvent:
        :return:
        """
        #print(QKeyEvent.key())
        if (QKeyEvent.key() == 16777220 or QKeyEvent.key() ==16777221):
            self.login()
    def displayInfo(self,info,status=None,lineFeed=None):
        """
        功能：用于将传递过来的info显示在QTextEdit上
        :param info:
        :return:
        """
        display_info=self.ui.display_info
        if len(display_info.toPlainText())>256:
            display_info.setHtml("")
        if not status:
            text = display_info.toHtml()+'<div style="color:#9900ff;">'+info+'</div>'
        elif status:
            text = display_info.toHtml()+'<div style="color:#cc0033;">'+info+'</div>'
        if lineFeed:
            if status:
                text = display_info.toHtml()+'<span style="color:#cc0033;">'+info+'</span>'
            else:
                text = display_info.toHtml()+'<span style="color:#cc0033;">'+info+'</span>'

        display_info.setHtml(text)
        display_info.moveCursor(QTextCursor.End)



class ThreadLogin(QThread):
    closeSignal=pyqtSignal()
    closeDialogSignal=pyqtSignal()
    displaySignal=pyqtSignal(str,bool,bool)
    def __init__(self,student_num=None,password=None,parent=None):
        super().__init__(parent)
        self.threadDonghua=threading.Thread(target=self.displayDongHua)#创建一个动画线程
        self.flag=True
        self.student_num=student_num
        self.password=password
    def run(self):
        self.threadDonghua.start()#开始执行动画线程
        # 创建爬虫登陆对象
        sprider = SpriderLogin(self.student_num, self.password)
        status = sprider.startLogin()
        self.flag = False#认证完成，关闭动画
        # self.flag = False
        # 如果登陆失败
        if not status:
            self.displaySignal.emit('认证失败，请检查用户名或者密码',True,False)#在界面上显示认证成功信息
            # self.displayInfo('认证失败！请检查你的账号密码是否正确！', True)
        else:
            # self.closeDialogSignal.emit()#关闭对话框
            # while True:pass
            self.displaySignal.emit('认证成功！程序将会在3秒钟之后自动退出',False,False)#在界面上显示认证成功信息
            time.sleep(3)#延时3秒
            self.closeDialogSignal.emit()#关闭对话框
            self.closeSignal.emit()#关闭程序
            # self.displayInfo('认证成功！程序将会在3秒钟之后自动退出', False)
            # self.closeWindowTimer.start()
    def displayDongHua(self):
        while self.flag:
            for i in range(30):
                if i == 26:
                    print('=======正在认证当中========')
                    continue
                for j in range(i):
                    pass
                    print("=", end="")
                print("")
                time.sleep(0.01)
            time.sleep(2)
        print('===========认证结束============')



class SpriderLogin(object):
    """
    功能：用于登陆的核心方法
    """
    def __init__(self,student_number,password):
        # 创建也给存储cookie的对象
        cookie = cookiejar.CookieJar()
        # 构建cookie的处理对象
        cookie_handler = request.HTTPCookieProcessor(cookie)
        # 构建自定义给opener
        self.opener = request.build_opener(cookie_handler)
        #学号
        self.student_number=student_number
        #密码
        self.password=password
    # 获取一个随机的Agent
    def getAgent(self):
        # 创建一个user-agent池
        ua_list = [
            "User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",  # Firefox 4.0.1 – Windows
            "User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",  # Opera 11.11 – Windows
            "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",  # 傲游（Maxthon）
            "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",  # 腾讯TT
            "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",  # 世界之窗（The World） 3.x
            "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
            # 搜狗浏览器 1.x
            "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"  # 360浏览器
        ]
        return random.choice(ua_list)

    def sendLoginRequest(self):
        """
        功能：发送登陆请求
        :return:返回登陆请求对象
        """
        # 构建登陆信息
        user_info = {'userName': self.student_number, 'pwd': self.password, 'opr': 'pwdLogin', 'rememberPwd': '0'}
        # 比特量化登陆信息
        data = parse.urlencode(user_info).encode('utf-8')
        # 访问的认证页面地址
        url = "http://1.1.1.3/ac_portal/login.php"
        # 创建访问对象
        re = request.Request(url, data=data, headers={'User-Agent': self.getAgent()})
        # 获取请求结果
        response = self.opener.open(re)
        #返回请求对象
        return response
    def verificationLogin(self,response):
        """
        功能：验证登陆结果
        :param response: 请求对象
        :return: 登陆结果，成功：Ture，否则：False
        """
        #验证结果标识b
        status=False
        result = response.read().decode()
        #print("返回结果：%s\n" % result)
        # 由于在python里面假：False，而他返回的是false,所以在将他装换成字典之前需要将他的第一个字母转换成False。
        #构建一个正则表达式对象，用于替换字符串
        pattern = re.compile('false')
        result = pattern.sub('False', result)
        # 如果转换失败，说明里面出现了true，这代表认证成功。
        try:
            result = eval(result)  # 将字符串转换位字典
        except Exception:
            #验证成功
            status=True
        return status
    def startLogin(self):
        #获取请求对象
        response=self.sendLoginRequest()
        #获取登陆结果
        status=self.verificationLogin(response)
        return status



def login(student_num,password):
    """
    用于创建登陆线程
    :param student_num:
    :param password:
    :return:
    """
    login = ThreadLogin(student_num, password)
    # 关联显示信息信号
    login.displaySignal.connect(widget.displayInfo)
    # 关联关闭程序信号
    login.closeSignal.connect(widget.closeWindow)
    login.start()
def getExePath():
    """
    功能：为了防止程序在自启动时，读取配置文件时，不能正确获取程序路径的方法。
    调用此方法可以获取到正确的程序路径
    :return:
    """
    sap = '/'
    if sys.argv[0].find(sap) == -1:
        sap = '\\'
    indx = sys.argv[0].rfind(sap)
    path = sys.argv[0][:indx] + sap
    return path

if __name__ == '__main__':
    #创建一个应用程序对象
    app=QApplication(sys.argv)
    #构建一个主界面对象
    widget=loginUI()
    #显示主界面
    widget.show()
    widget.setWindowTitle("上网认证 By：DZ5141柒月")
    widget.loginSignal.connect(login)
    #为了防止在检测WIFI时界面卡死，所以在这里使用了多线程UI+信号机制
    #构造一个每过1秒就触发一次的定时器，用于检查当前的Wifi条件是否符合。
    CheckWifiThread = Mythread(UI=widget)
    # 关联显示信号
    CheckWifiThread.breakSignal.connect(widget.displayInfo)
    # 关联自动登陆信号
    CheckWifiThread.loginSignal.connect(widget.autoLogin)
    # 执行
    CheckWifiThread.start()
    # 这里也为了防止界面发生无响应或者卡死情况，在这里使用了多线程UI+信号机制来
    sys.exit(app.exec_())
