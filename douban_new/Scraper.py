#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore,QtGui
from pymongo import MongoClient
import subprocess
import os
import datetime
import threading
import redis

import Scraper_rc


class TimeThread_c(QtCore.QThread):
    signal_time = QtCore.pyqtSignal(str, int) # 信号
 
    def __init__(self, index, parent=None):
        super(TimeThread_c, self).__init__(parent)
	self.index = index
 
   
    def run(self):

        self.success=True
        client=MongoClient()
        db=client.douban_crawler
        
        if os.path.exists("./Scraper.py"):
            os.chdir("douban_movie/movie_crawler/")
           
   	if self.index == 0:   
            p=subprocess.Popen("scrapy crawl movieLinks",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

        else:
            p=subprocess.Popen("scrapy crawl movieContent",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

        client.close()

class TimeThread_r(QtCore.QThread):
    signal_time = QtCore.pyqtSignal(str, int) # 信号
 
    def __init__(self, index, parent=None):
        super(TimeThread_r, self).__init__(parent)
	self.index = index
 
   
    def run(self):

        self.success=True
        client=MongoClient()
        db=client.douban_crawler
        
        if os.path.exists("./Scraper.py"):
            os.chdir("douban_movie/movie_crawler/")
           
   	if self.index == 0:   
            p=subprocess.Popen("scrapy crawl reviewLinks",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

        else:
            p=subprocess.Popen("scrapy crawl review",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

        client.close()    

class ShowThread_c(QtCore.QThread):
    signal_time = QtCore.pyqtSignal(int, int) # 信号
 
    def __init__(self, index, parent=None):
        super(ShowThread_c, self).__init__(parent)
	self.index = index
 
    def start_timer(self):
        self.count_2 = 0
        self.start()

    def run(self):

        r = redis.Redis(host='127.0.0.1',port=6379,db=0)
        
        self.sleep(5)
   
   	if self.index == 0:   
            while True:
                self.count_1 = r.llen('movie_links')
                if self.count_1 > self.count_2:
                    self.num = self.count_1 - self.count_2
                    self.signal_time.emit(self.num,self.count_1)
                    self.count_2 = self.count_1
                    self.sleep(3)

        else:
            while True:
                self.count_1 = r.llen('movieContent:items')
                if self.count_1 > self.count_2:
                    self.num = self.count_1 - self.count_2
                    self.signal_time.emit(self.num,self.count_1)
                    self.count_2 = self.count_1
                    self.sleep(3)
               
        client.close()

class ShowThread_r(QtCore.QThread):
    signal_time = QtCore.pyqtSignal(int, int) # 信号
 
    def __init__(self, index, parent=None):
        super(ShowThread_r, self).__init__(parent)
	self.index = index
 
    def start_timer(self):
        self.count_2 = 0
        self.start()

    def run(self):

        r = redis.Redis(host='127.0.0.1',port=6379,db=0)
        
        self.sleep(5)
   
   	if self.index == 0:   
            while True:
                self.count_1 = r.llen('review_links')
                if self.count_1 > self.count_2:
                    self.num = self.count_1 - self.count_2
                    self.signal_time.emit(self.num,self.count_1)
                    self.count_2 = self.count_1
                    self.sleep(3)

        else:
            while True:
                self.count_1 = r.llen('review:items')
                if self.count_1 > self.count_2:
                    self.num = self.count_1 - self.count_2
                    self.signal_time.emit(self.num,self.count_1)
                    self.count_2 = self.count_1
                    self.sleep(3)
               
        client.close()

class CrawlContentPage(QtGui.QWidget):
    def __init__(self, parent=None):
        super(CrawlContentPage, self).__init__(parent)
       
        self.success=True
        
        #爬虫布局
        crawlGroup = QtGui.QGroupBox(u"豆瓣内容爬虫")
        serverLabel = QtGui.QLabel(u"爬取类型:")
        self.serverCombo = QtGui.QComboBox()
        self.serverCombo.addItem(u"电影链接爬取")
        self.serverCombo.addItem(u"电影内容爬取")

        startButton=QtGui.QPushButton(u"开始")
        self.textEdit = QtGui.QTextEdit()
        self.textEdit.setMaximumHeight(150)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")

        startButton.clicked.connect(self.click)

        crawlLayout = QtGui.QVBoxLayout()
        crawlLayout.addWidget(serverLabel)
        crawlLayout.addWidget(self.serverCombo)
        crawlLayout.addWidget(startButton)
        crawlLayout.addWidget(self.textEdit)
        crawlGroup.setLayout(crawlLayout)

        #网站分析
        parameterGroup=QtGui.QGroupBox(u"相关参数")
    
        fieldList= QtGui.QListWidget()
    
        MovieNameItem=QtGui.QListWidgetItem(fieldList)
        MovieNameItem.setText("MovieName")
        urlItem=QtGui.QListWidgetItem(fieldList)
        urlItem.setText("url")
        PostUrlItem=QtGui.QListWidgetItem(fieldList)
        PostUrlItem.setText("PostUrl")
        DirectorItem=QtGui.QListWidgetItem(fieldList)
        DirectorItem.setText("Director")
        ReleaseTimeItem=QtGui.QListWidgetItem(fieldList)
        ReleaseTimeItem.setText("ReleaseTime")
        AreaItem=QtGui.QListWidgetItem(fieldList)
        AreaItem.setText("Area")
        PerformersItem=QtGui.QListWidgetItem(fieldList)
        PerformersItem.setText("Performers")
        RateItem=QtGui.QListWidgetItem(fieldList)
        RateItem.setText("Rate")

        superviserButton=QtGui.QPushButton(u"监控")
        superviserButton.clicked.connect(self.superviser)        

        parameterLayout= QtGui.QVBoxLayout()
        parameterLayout.addWidget(fieldList)
        parameterLayout.addWidget(superviserButton)
        parameterGroup.setLayout(parameterLayout)
        
        
      
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(crawlGroup)
        mainLayout.addWidget(parameterGroup)
        mainLayout.addSpacing(12)
        mainLayout.addStretch(1)
        
        self.setLayout(mainLayout)
 

    def superviser(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://127.0.0.1:8888/index.html'))


    def click(self):
	self.thread = TimeThread_c(self.serverCombo.currentIndex())
        self.show = ShowThread_c(self.serverCombo.currentIndex())
        self.show.signal_time.connect(self.showResult)
	self.thread.start()
        self.show.start_timer()
       


    def showResult(self,number,total):
    
        if self.serverCombo.currentIndex() == 0:
            self.textEdit.setText(str(number) + u"条新电影链接被爬取 \n" + str(total) + u"条电影链接一共被爬取")
        else:            
             self.textEdit.setText(str(number) + u"条新电影内容被爬取 \n" + str(total) + u"条电影内容一共被爬取")

        

class CrawlReviewPage(QtGui.QWidget):
    def __init__(self, parent=None):
        super(CrawlReviewPage, self).__init__(parent)
        self.success=True
        #爬虫布局
        crawlGroup = QtGui.QGroupBox(u"豆瓣评论爬虫")
        serverLabel = QtGui.QLabel(u"爬取年份")
        self.serverCombo = QtGui.QComboBox()
        self.serverCombo.addItem("1990")
        self.serverCombo.addItem("1991")
        self.serverCombo.addItem("1992")
        self.serverCombo.addItem("1993")
        self.serverCombo.addItem("1994")
        self.serverCombo.addItem("1995")
        self.serverCombo.addItem("1996")
        self.serverCombo.addItem("1997")
        self.serverCombo.addItem("1998")
        self.serverCombo.addItem("1999")
        self.serverCombo.addItem("2000")
        self.serverCombo.addItem("2001")
        self.serverCombo.addItem("2002")
        self.serverCombo.addItem("2003")
        self.serverCombo.addItem("2004")
        self.serverCombo.addItem("2005")
        self.serverCombo.addItem("2006")
        self.serverCombo.addItem("2007")
        self.serverCombo.addItem("2008")
        self.serverCombo.addItem("2009")
        self.serverCombo.addItem("2010")
        self.serverCombo.addItem("2011")
        self.serverCombo.addItem("2012")
        self.serverCombo.addItem("2013")
        self.serverCombo.addItem("2014")
        self.serverCombo.addItem("2015")
        self.serverCombo.addItem("2016")
        insertButton=QtGui.QPushButton(u"导入年份")

        serverLayout = QtGui.QHBoxLayout()
        serverLayout.addStretch(1)
        serverLayout.addWidget(serverLabel)
        serverLayout.addWidget(self.serverCombo)

        typeLabel = QtGui.QLabel(u"爬取类型:")
        self.typeCombo = QtGui.QComboBox()
        self.typeCombo.addItem(u"评论链接爬取")
        self.typeCombo.addItem(u"评论内容爬取")

        typeLayout = QtGui.QHBoxLayout()
        typeLayout.addStretch(1)
        typeLayout.addWidget(typeLabel)
        typeLayout.addWidget(self.typeCombo)

        startButton=QtGui.QPushButton(u"开始")
        self.textEdit = QtGui.QTextEdit()
        self.textEdit.setMaximumHeight(150)
        self.textEdit.setReadOnly(True)

        insertButton.clicked.connect(self.insert)

        startButton.clicked.connect(self.click)
        
        crawlLayout = QtGui.QVBoxLayout()
        crawlLayout.addLayout(serverLayout)
        crawlLayout.addLayout(typeLayout)
        crawlLayout.addWidget(insertButton)
        crawlLayout.addWidget(startButton)
        crawlLayout.addWidget(self.textEdit)
        crawlGroup.setLayout(crawlLayout)

        #网站分析
        parameterGroup=QtGui.QGroupBox(u"相关参数")
    
        fieldList= QtGui.QListWidget()
    
        MovieNameItem=QtGui.QListWidgetItem(fieldList)
        MovieNameItem.setText("MovieName")
        urlItem=QtGui.QListWidgetItem(fieldList)
        urlItem.setText("url")
        MovieLinkItem=QtGui.QListWidgetItem(fieldList)
        MovieLinkItem.setText("MovieLink")
        ReviewTitleItem=QtGui.QListWidgetItem(fieldList)
        ReviewTitleItem.setText("ReviewTitle")
        ReviewAuthorItem=QtGui.QListWidgetItem(fieldList)
        ReviewAuthorItem.setText("ReviewAuthor")
        AuthorLinkItem=QtGui.QListWidgetItem(fieldList)
        AuthorLinkItem.setText("AuthorLink")
        ReviewContentItem=QtGui.QListWidgetItem(fieldList)
        ReviewContentItem.setText("ReviewContent")
        UpNumberItem=QtGui.QListWidgetItem(fieldList)
        UpNumberItem.setText("UpNumber")
        DownNumberItem=QtGui.QListWidgetItem(fieldList)
        DownNumberItem.setText("DownNumber")
        RateItem=QtGui.QListWidgetItem(fieldList)
        RateItem.setText("Rate")
        
        superviserButton=QtGui.QPushButton(u"监控")


       # self.table=QtGui.QTableWidget(0,4)
       # self.table.setMinimumHeight(450)

        
        superviserButton.clicked.connect(self.superviser)
        
        parameterLayout=QtGui.QVBoxLayout()
        parameterLayout.addWidget(fieldList)
        parameterLayout.addWidget(superviserButton)
        parameterGroup.setLayout(parameterLayout)
      
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(crawlGroup)
        mainLayout.addWidget(parameterGroup)
        mainLayout.addSpacing(12)
        mainLayout.addStretch(1)

       
        self.setLayout(mainLayout)

    def superviser(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://127.0.0.1:8888/index.html'))


    def insert(self):
        if os.path.exists("./Scraper.py"):
            os.chdir("douban_movie/movie_crawler/review_links")
        with open(self.serverCombo.currentText(), 'r') as f:
            lines = f.readlines()
            for line in lines:
                os.system('redis-cli -a kNlTR2nPrv lpush more_reviews ' + line + '/') 

    def click(self):
	self.thread = TimeThread_r(self.typeCombo.currentIndex())
        self.show = ShowThread_r(self.typeCombo.currentIndex())
        self.show.signal_time.connect(self.showResult)
	self.thread.start()
        self.show.start_timer()
       

    def showResult(self,number,total):
    
        if self.typeCombo.currentIndex() == 0:
            self.textEdit.setText(str(number) + u"条新评论链接被爬取 \n" + str(total) + u"条评论链接一共被爬取")
        else:            
             self.textEdit.setText(str(number) + u"条新评论内容被爬取 \n" + str(total) + u"条评论内容一共被爬取")

       


class QueryPage(QtGui.QWidget):
    def __init__(self, parent=None):
        super(QueryPage, self).__init__(parent)

        packagesGroup = QtGui.QGroupBox(u"查询")

        actorLabel = QtGui.QLabel(u"演员:")
        self.actorEdit = QtGui.QLineEdit()

        movieNameLabel = QtGui.QLabel(u"电影名称:")
        self.movieNameEdit = QtGui.QLineEdit()

        self.fromDateEdit = QtGui.QDateEdit()
        self.fromDateEdit.setDate(QtCore.QDate(2015, 1, 1))
        self.fromDateEdit.setCalendarPopup(True)
        fromLabel = QtGui.QLabel(u"时间起始:")
        fromLabel.setBuddy(self.fromDateEdit)
        self.toDateEdit = QtGui.QDateEdit()
        self.toDateEdit.setDate(QtCore.QDate.currentDate())
        self.toDateEdit.setCalendarPopup(True)
        toLabel = QtGui.QLabel(u"截至:")
        toLabel.setBuddy(self.toDateEdit)


        startQueryButton = QtGui.QPushButton(u"开始查询")
        clearQueryButton=QtGui.QPushButton(u"清除结果")

        #结果布局
        resultGroup=QtGui.QGroupBox(u"爬虫结果")
        self.table=QtGui.QTableWidget(0,4)
        self.table.setMinimumHeight(450)
        headerLabels = (u"电影名称", u"演员",u"上映日期",u"地区/国家")
        self.table.setHorizontalHeaderLabels(headerLabels)
        self.table.setColumnWidth(0,400)
        self.table.setColumnWidth(1,200)
        #改变颜色
        self.table.setAlternatingRowColors(True)
        #self.table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        resultLayout=QtGui.QVBoxLayout()
        resultLayout.addWidget(self.table)
        resultGroup.setLayout(resultLayout)

        packagesLayout = QtGui.QGridLayout()
        packagesLayout.addWidget(movieNameLabel, 0, 0)
        packagesLayout.addWidget(self.movieNameEdit, 0, 1)
        packagesLayout.addWidget(actorLabel, 0, 2)
        packagesLayout.addWidget(self.actorEdit, 0, 3)
        packagesLayout.addWidget(fromLabel, 1, 0)
        packagesLayout.addWidget(self.fromDateEdit, 1, 1, 1, 1)
        packagesLayout.addWidget(toLabel, 1, 2)
        packagesLayout.addWidget(self.toDateEdit, 1, 3, 1, 1)
        packagesLayout.addWidget(startQueryButton,2,1)
        packagesLayout.addWidget(clearQueryButton,2,3)
        
        packagesGroup.setLayout(packagesLayout)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(packagesGroup)
        mainLayout.addWidget(resultGroup)
        mainLayout.addSpacing(12)
        mainLayout.addStretch(1)

        self.showResult(False,queryCollection=[])
        startQueryButton.clicked.connect(self.queryResult)
        clearQueryButton.clicked.connect(self.clearResult)       
        self.setLayout(mainLayout)

    def queryResult(self):
        movieName=unicode(self.movieNameEdit.text())
        actor=unicode(self.actorEdit.text())
        fromDate=unicode(self.fromDateEdit.date().toString("yyyy-MM-dd"))
        toDate=unicode(self.toDateEdit.date().toString("yyyy-MM-dd"))
        
        client=MongoClient()
        db=client.douban_crawler
        collection=db.douabn_crawler
        if movieName!="" and actor=="":
            queryCollection=db.douban_crawler.find({"ReleaseTime":{"$gte":str(fromDate),"$lte":str(toDate)},"MovieName":{"$regex":movieName}})
        elif movieName!="" and actor!="":
            queryCollection=db.douban_crawler.find({"ReleaseTime":{"$gte":str(fromDate),"$lte":str(toDate)},"MovieName":{"$regex":movieName},"Performers":{"$regex":actor}})
        elif movieName=="" and actor!="":
            queryCollection=db.douban_crawler.find({"ReleaseTime":{"$gte":str(fromDate),"$lte":str(toDate)},"Performers":{"$regex":actor}})
        else:
            queryCollection=db.douban_crawler.find({"ReleaseTime":{"$gte":str(fromDate),"$lte":str(toDate)}})
        self.showResult(True,queryCollection)
        client.close()

    def clearResult(self):
        self.table.clearContents()

    def showResult(self,isShow,queryCollection):
        if not isShow:
            return
       
        self.table.setRowCount(queryCollection.count())
        row=0
        for p in queryCollection:
            item0=QtGui.QTableWidgetItem(p.get("MovieName","-1"))
            item1=QtGui.QTableWidgetItem(p.get("Performers","-1"))
            item2=QtGui.QTableWidgetItem(p.get("ReleaseTime","-1"))
            item3=QtGui.QTableWidgetItem(p.get("Area","-1"))
            self.table.setItem(row,0,item0)
            self.table.setItem(row,1,item1)
            self.table.setItem(row,2,item2)
            self.table.setItem(row,3,item3)
            row=row+1


class ConfigDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)
        self.setFixedSize(1024,705)
        self.contentsWidget = QtGui.QListWidget()
        self.contentsWidget.setViewMode(QtGui.QListView.IconMode)
        self.contentsWidget.setIconSize(QtCore.QSize(96, 84))
        self.contentsWidget.setMovement(QtGui.QListView.Static)
        self.contentsWidget.setMaximumWidth(128)
        self.contentsWidget.setSpacing(12)

        self.pagesWidget = QtGui.QStackedWidget()
        self.pagesWidget.addWidget(CrawlContentPage())
        self.pagesWidget.addWidget(CrawlReviewPage())
        self.pagesWidget.addWidget(QueryPage())

        clearButton = QtGui.QPushButton(u"清空数据库")
        closeButton = QtGui.QPushButton(u"关闭")

        self.createIcons()
        self.contentsWidget.setCurrentRow(1)

        clearButton.clicked.connect(self.clear)
        closeButton.clicked.connect(self.close)

        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.addWidget(self.contentsWidget)
        horizontalLayout.addWidget(self.pagesWidget, 1)

        buttonsLayout = QtGui.QHBoxLayout()
        buttonsLayout.addStretch(1)
        buttonsLayout.addWidget(clearButton)
        buttonsLayout.addWidget(closeButton)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(horizontalLayout)
        mainLayout.addStretch(1)
        mainLayout.addSpacing(12)
        mainLayout.addLayout(buttonsLayout)

        self.setLayout(mainLayout)

        self.setWindowTitle(u"豆瓣电影爬虫")

    def clear(self):
        #删除原有数据
        client=MongoClient()
        db=client.douban_crawler
        db.douban_crawler.remove()


    def changePage(self, current, previous):
        if not current:
            current = previous

        self.pagesWidget.setCurrentIndex(self.contentsWidget.row(current))

    def createIcons(self):
        configButton = QtGui.QListWidgetItem(self.contentsWidget)
        configButton.setIcon(QtGui.QIcon(u':/images/Content.png'))
        configButton.setText(u"豆瓣内容爬虫")
        configButton.setTextAlignment(QtCore.Qt.AlignHCenter)
        configButton.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        updateButton = QtGui.QListWidgetItem(self.contentsWidget)
        updateButton.setIcon(QtGui.QIcon(u':/images/Review.png'))
        updateButton.setText(u"豆瓣评论爬虫")
        updateButton.setTextAlignment(QtCore.Qt.AlignHCenter)
        updateButton.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        queryButton = QtGui.QListWidgetItem(self.contentsWidget)
        queryButton.setIcon(QtGui.QIcon(u':/images/query.png'))
        queryButton.setText(u"查询")
        queryButton.setTextAlignment(QtCore.Qt.AlignHCenter)
        queryButton.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        self.contentsWidget.currentItemChanged.connect(self.changePage)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    dialog = ConfigDialog()
    sys.exit(dialog.exec_()) 
