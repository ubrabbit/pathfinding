#coding: utf-8

import sys
import copy
import math
import re
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont, QIcon

import c_path

from Common import *


class CPainter(QtWidgets.QWidget):

    m_Path_Color="#55ff7f"

    def __init__(self,grid,parent=None):
        super(CPainter,self).__init__(parent)

        self.m_Grid = grid
        self.m_Row,self.m_Col=self.m_Grid.m_Row, self.m_Grid.m_Col
        print("self.m_Row,self.m_Col>>>>>>>>>>>>>>>>.   ",self.m_Row,self.m_Col)

        #剩余路径列表
        self.m_PathList=[]
        self.m_PathList_Bak=[]
        #已经经过的路径列表，初始为出口
        self.m_PassList=[]

        self.m_ColorBackup={}

        self.setWindowTitle(self.tr("显示窗口"))

        mainLayout=QtWidgets.QHBoxLayout(self)
        leftLayout=QtWidgets.QVBoxLayout()
        rightLayout=QtWidgets.QVBoxLayout()

        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.m_WindowSize_Col=screen.width()
        self.m_WindowSize_Row=screen.height()
        self.PaintMap()

        bottomLayout=QtWidgets.QHBoxLayout()
        leftLayout.addWidget(self.mapWidget)
        leftLayout.addLayout(bottomLayout)
        leftLayout.setStretchFactor(self.mapWidget,19)
        leftLayout.setStretchFactor(bottomLayout,1)

        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)
        mainLayout.setStretchFactor(leftLayout,19)
        mainLayout.setStretchFactor(rightLayout,1)

        sList=[
        ("开始","Paint_Start"),
        ]
        oList=[]
        for sName,sKey in sList:
            oButton=QtWidgets.QPushButton(self.tr(sName))
            func=partial(self.OnButtonClicked,sKey)
            oButton.clicked.connect(func)
            oList.append(oButton)
            setattr(self,"m_Button_%s"%sKey,oButton)
            if sKey!="Paint_Start":
                oButton.setEnabled(False)

        rightLayout.addStretch(1)
        for oButton in oList:
            rightLayout.addWidget(oButton)
        for oButton in oList:
            rightLayout.setStretchFactor(oButton,1)

        layout_cost=QtWidgets.QHBoxLayout()
        label1=QtWidgets.QLabel(self.tr("c层寻路开销："))
        label2=QtWidgets.QLabel(self.tr("0"))
        label3=QtWidgets.QLabel(self.tr(" ms"))
        self.costLabel=label2
        label1.setFont(QFont('微软雅黑',10))
        label2.setFont(QFont('微软雅黑',10))
        label3.setFont(QFont('微软雅黑',10))
        layout_cost.addWidget(label1)
        layout_cost.addWidget(label2)
        layout_cost.addWidget(label3)
        rightLayout.addLayout(layout_cost)

        #layout_search=QtWidgets.QHBoxLayout()
        #label1=QtWidgets.QLabel(self.tr("搜索格子数量："))
        #label2=QtWidgets.QLabel(self.tr("0"))
        #self.searchLabel=label2
        #label1.setFont(QFont('微软雅黑',10))
        #label2.setFont(QFont('微软雅黑',10))
        #layout_search.addWidget(label1)
        #layout_search.addWidget(label2)
        #rightLayout.addLayout(layout_search)

        layout_path=QtWidgets.QHBoxLayout()
        label1=QtWidgets.QLabel(self.tr("路径经过的格子数："))
        label2=QtWidgets.QLabel(self.tr("0"))
        self.pathLabel=label2
        label1.setFont(QFont('微软雅黑',10))
        label2.setFont(QFont('微软雅黑',10))
        layout_path.addWidget(label1)
        layout_path.addWidget(label2)
        rightLayout.addLayout(layout_path)
        rightLayout.addStretch(5)

        self.MoveAll_timer=QtCore.QTimer()
        #设置窗口计时器
        self.MoveAll_timer.timeout.connect(self.MoveAllNext)

        iWidth,iHeight=screen.width()*3/4, screen.height()*3/4
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.resize(iWidth,iHeight)
        self.setFixedSize(iWidth,iHeight)
        self.move(0,0)

    def OnButtonClicked(self,sFlag):
        print("OnButtonClicked ",sFlag)
        if sFlag=="Paint_Start":
            self.MoveStart()

    def PaintMap(self):
        self.mapWidget=QtWidgets.QTableWidget(self)
        self.mapWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.PaintTables()
        self.RegistMap()

    def PaintTables(self):
        self.progressDialog=QtWidgets.QProgressDialog(self)
        self.progressDialog.setWindowModality(QtCore.Qt.WindowModal)
        #设置进度对话框出现等待时间，此处设定为 5 秒，默认为 4 秒
        self.progressDialog.setMinimumDuration(5)
        self.progressDialog.setWindowTitle(self.tr("请等待"))
        self.progressDialog.setLabelText(self.tr("读取..."))
        self.progressDialog.setCancelButtonText(self.tr("取消"))
        self.progressDialog.setRange(0,10)

        self.mapWidget.setRowCount(self.m_Row)
        self.mapWidget.setColumnCount(self.m_Col)

        iRowSize=max(15,min(20,self.m_WindowSize_Row/self.m_Row))
        iColSize=max(15,min(20,self.m_WindowSize_Col/self.m_Col))
        for col in range(self.m_Col):
                self.mapWidget.setColumnWidth(col,iColSize)
        for row in range(self.m_Row):
                self.mapWidget.setRowHeight(row,iRowSize)

        posList=self.m_Grid.GetPosList()
        blockList=self.m_Grid.GetBlockList()

        ilen1=len(posList)
        ilen2=len(blockList)
        for i in range(10+1):
            self.progressDialog.setValue(i)
            if self.progressDialog.wasCanceled():
                self.mapWidget.clear()
                return

            j=ilen1/10
            while(posList and j>=0):
                j-=1
                row,col,cost=posList.pop(0)
                pos=(row,col)
                iColor=self.m_Grid.GetPosColor(pos)
                if not iColor:
                    continue
                sColor=GridColorList[iColor]
                self.SetColor(row,col,sColor)
                self.m_ColorBackup[pos]=sColor
            j=ilen2/10
            while(blockList and j>=0):
                j-=1
                pos=blockList.pop(0)
                row,col=pos
                sColor=ColorBlock
                self.SetColor(row,col,sColor)
                self.m_ColorBackup[pos]=sColor
        self.progressDialog.cancel()

    #把 (row,col) 格式显示的格子转换成 (x,y) 格式的坐标系
    def FormatMapPos(self, posSource):
        if isinstance(posSource, tuple) and len(posSource) == 2:
            row,col = posSource
            return (col,row)
        posList = []
        for pos in posSource:
            pos1 = list(pos)
            pos1[1], pos1[0] = pos1[0], pos1[1]
            posList.append( tuple( pos1 ) )
        return posList

    def RegistMap(self):
        posList = self.FormatMapPos(self.m_Grid.GetPosList())
        blockList = self.FormatMapPos(self.m_Grid.GetBlockList())
        print("CreateMap:  %s * %s"%(self.m_Col,self.m_Row))
        print("posList:  ",posList)
        print("blockList:  ",blockList)
        try:
            iret=c_path.CreateMap(self.m_Col,self.m_Row,posList,blockList)
            assert(iret==1)
        except Exception as err:
            print("CreateMap error")
            debug_print()

    def SetColor(self,row,col,sColor):
        owidget=QtWidgets.QWidget()
        owidget.setStyleSheet('QWidget {background-color:%s}'%sColor)
        self.mapWidget.setCellWidget(row,col,owidget)
        return 1

    def MoveStart(self):
        self.m_Start=1
        self.m_Button_Paint_Start.setEnabled(False)

        self.MoveAll_timer.stop()
        if not self.m_Grid.m_PosEntrance or not self.m_Grid.m_PosExport:
            QtWidgets.QMessageBox.information(self,"无结果",self.tr("无效的起点与终点"))
            return
        try:
            totalCost = 0
            for i in range(100):
                posEnter = self.FormatMapPos(self.m_Grid.m_PosEntrance)
                posExit = self.FormatMapPos(self.m_Grid.m_PosExport)
                iCost, pTuple=c_path.SeekPath( posEnter, posExit )
                print(">>>> Cost  ",iCost)
                totalCost+=iCost
        except Exception as err:
            print("SeekPath error")
            debug_print()
            QtWidgets.QMessageBox.information(self,"无结果",self.tr("SeekPath调用出错"))
            return

        pList=list(pTuple)
        print("totalCost  ",totalCost)
        print("pTuple  ",pTuple)

        if not pList:
            row_enter,col_enter=self.m_Grid.m_PosEntrance
            row_exit,col_exit=self.m_Grid.m_PosExport
            if( abs(row_enter-row_exit) + abs(col_enter-col_exit) <=2 ):
                QtWidgets.QMessageBox.information(self,"结果",self.tr("入口就在出口旁边"))
                return
            QtWidgets.QMessageBox.information(self,"无结果",self.tr("入口到出口无可达路径"))
            return
        self.costLabel.setText("%s"%totalCost )

        self.m_PathList=[]
        while (pList):
            i,j=pList.pop(0),pList.pop(0)
            self.m_PathList.append( (i,j) )
        self.pathLabel.setText("%s"%len(self.m_PathList) )
        self.m_PathList_Bak=self.m_PathList[:]
        self.MoveAll()

    def MoveNextStep(self):
        if not getattr(self,"m_Start",0):
            return 0
        if not self.m_PathList:
            return 0
        col,row=self.m_PathList.pop(0)
        self.m_PassList.append( (row,col) )
        self.SetColor(row,col,self.m_Path_Color)
        return 1

    def MoveAll(self):
        import time
        if not getattr(self,"m_Start",0):
            return
        self.m_Button_Paint_Start.setEnabled(False)
        self.MoveAllNext()

    def MoveAllNext(self):
        self.MoveAll_timer.stop()
        if( self.MoveNextStep() ):
            self.MoveAll_timer.start(5)
        self.update()
