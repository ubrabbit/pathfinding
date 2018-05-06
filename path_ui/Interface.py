#coding: utf-8

"""
/*
 *  Copyright (C) 2011-2017 ubrabbit
 *  Author: ubrabbit <ubrabbit@gmail.com>
 *  Date: 2017-01-22 12:49:09
 *
 */

"""

import sys
import copy
import math
import re
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import qApp, \
                            QWidget, QTabWidget, QHBoxLayout, QListWidget, QStackedWidget, QVBoxLayout, \
                            QTextEdit, QTableWidget, QAbstractItemView, QLabel, QComboBox, QLineEdit, \
                            QPushButton, QAction, QFileDialog, QMessageBox, QProgressDialog
from PyQt5.QtGui import QFont, QIcon
#显示中文
QtCore.QTextCodec.setCodecForLocale(QtCore.QTextCodec.codecForName("system"))

import Console
import HelpWindow
from Painter import CPainter
from Grid import CGrid

from Common import *


class CApp(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.m_Grid=CGrid(self)
        self.m_Interface=CInterface(self)

        self.setWindowTitle(self.tr("寻路显示器"))

        screen = QtWidgets.QDesktopWidget().screenGeometry()
        #self.resize(screen.width(), screen.height())
        self.resize(screen.width()*3/4, screen.height()*3/4)

    def __del__(self):
        Console.ConsoleFree()

    def ImportTxtFile(self):
        sFilter="Text Files(*.txt)"
        fileName=QFileDialog.getOpenFileName(self,self.tr("打开文件"),"",self.tr(sFilter))
        print("fileName is ",fileName)
        fileName = fileName[0]
        if not fileName:
            return

        self.m_Interface.label_File.setText(fileName)

        self.progressDialog=QProgressDialog(self)
        self.progressDialog.setWindowModality(QtCore.Qt.WindowModal)
        #设置进度对话框出现等待时间，此处设定为 5 秒，默认为 4 秒
        self.progressDialog.setMinimumDuration(5)
        self.progressDialog.setWindowTitle(self.tr("请等待"))
        self.progressDialog.setLabelText(self.tr("读取..."))
        self.progressDialog.setCancelButtonText(self.tr("取消"))
        self.progressDialog.setRange(0,10)

        with open(fileName,"r") as fobj:
            sCode=fobj.read()
            iRow,iCol,dPos=self.m_Grid.LoadTxt(sCode)

            self.m_Interface.tableWidget.clear()
            self.m_Interface.ResetTableGridSize(iRow,iCol)

            posList=list(dPos.keys())
            ilen=len(dPos)
            for i in range(10+1):
                self.progressDialog.setValue(i)
                if self.progressDialog.wasCanceled():
                    self.m_Interface.tableWidget.clear()
                    return

                j=ilen/10
                while(posList and j>=0):
                    j-=1
                    pos=posList.pop(0)
                    iColor=dPos[pos]
                    row,col=pos
                    if not iColor:
                        continue
                    self.m_Interface.SetTableCellColor(row,col,iColor)
        self.m_Interface.showGraphStack.setCurrentIndex(1)
        QMessageBox.information(self,"成功",self.tr("导入文件%s成功！"%fileName))

    def ExportToTxtFile(self):
        errMessage = self.m_Grid.ValidPaint()
        if errMessage:
            QMessageBox.information(self,"输入错误",self.tr(errMessage))
            return

        sFilter=""
        fileName=QFileDialog.getOpenFileName(self,self.tr("打开文件"),"",self.tr(sFilter))
        print("fileName is ",fileName)
        fileName = fileName[0]
        if not fileName:
            return
        if fileName=="config":
            QMessageBox.information(self,"输入错误",self.tr("不能存入配置文件"))
            return

        with open(fileName,"w+") as fobj:
            sCode=self.m_Grid.SaveTxt()
            fobj.write(sCode)
        QMessageBox.information(self,"保存",self.tr("保存成功！"))

    def StartPainting(self):
        errMessage = self.m_Grid.ValidPaint()
        if errMessage:
            QMessageBox.information(self,"输入错误",self.tr(errMessage))
            return
        try:
            self.m_CurWindow=CPainter(self.m_Grid)
            self.m_CurWindow.show()
        except Exception as err:
            debug_print()

    def OpenHelpWindow(self):
        #需要保存为成员变量，不然会被释放
        self.m_CurWindow=HelpWindow.Open()
        self.m_CurWindow.show()

    def OpenAboutWindow(self):
        QMessageBox.about(self,self.tr("关于"),self.tr(self.GetAbout()))

    def GetAbout(self):
        sCode=\
"""
作者：ubrabbit
版本：%s
这是一个可以达成可视化寻路显示目的的界面程序
"""%self.GetVersion()
        return sCode

    def GetVersion(self):
        return "v%s"%VERSION

class CInterface(object):

    def __init__(self, parent):
        super( CInterface, self).__init__()
        self.m_Parent = parent

        self.m_CurSelectColor=0
        self.m_RowCnt=0
        self.m_ColCnt=0

        self.m_EntranceColor=0
        self.m_ExitColor=0
        self.m_BlockColor=0

        try:
            self.LayoutInit()
            self.InitGraphLayout()
            self.StatusBarInit()
        except Exception as e:
            Console.ConsoleFree()
            import traceback
            traceback.print_exc()
            #exit(-1)

    def LayoutInit(self):
        centralWidget=QWidget(self.m_Parent)
        self.m_Parent.setCentralWidget(centralWidget)

        self.tab_Widget=QTabWidget(self.m_Parent)
        self.mainLayout=QHBoxLayout(centralWidget)

        self.listWidget=QListWidget()
        self.showGraphStack=QStackedWidget()

        self.listWidget.insertItem(0,self.m_Parent.tr("说明"))
        self.listWidget.insertItem(1,self.m_Parent.tr("画图"))
        #self.m_Parent.connect(self.listWidget,QtCore.SIGNAL("currentRowChanged(int)"),self.showGraphStack,QtCore.SLOT("setCurrentIndex(int)"))
        self.listWidget.currentRowChanged.connect( self.showGraphStack.setCurrentIndex )

        self.mainLayout.addWidget(self.listWidget)
        self.mainLayout.addWidget(self.tab_Widget)
        #设置布局空间的比例
        self.mainLayout.setStretchFactor(self.listWidget,1)
        self.mainLayout.setStretchFactor(self.tab_Widget,29)

    def InitGraphLayout(self):
        console_Edit=QTextEdit()
        log_Edit=QTextEdit()
        self.console_Edit,self.log_Edit=console_Edit,log_Edit
        if DEFINE_REDIRECT_STDOUT:
            try:
                self.console_Edit,self.log_Edit=Console.ConsoleInit(self)
            except Exception as err:
                debug_print()

        graphWidget=QWidget(self.m_Parent)
        graphLayout=QVBoxLayout(graphWidget)

        tipWidget=QWidget(self.m_Parent)
        layout_Vertical=QVBoxLayout(tipWidget)
        layout_Horizon=QHBoxLayout()
        tips=QTextEdit()
        sText=self.m_Parent.GetAbout()
        tips.setText(self.m_Parent.tr(sText))
        tips.setEnabled(False)
        layout_Vertical.addWidget(tips)
        layout_Vertical.addLayout(layout_Horizon)
        layout_Vertical.addStretch(5)

        self.showGraphStack.addWidget(tipWidget)
        self.showGraphStack.addWidget(graphWidget)

        self.tab_Widget.addTab(self.showGraphStack,self.m_Parent.tr("画图"))
        if DEFINE_REDIRECT_STDOUT:
            self.tab_Widget.addTab(self.console_Edit,self.m_Parent.tr("控制台"))
            self.tab_Widget.addTab(self.log_Edit,self.m_Parent.tr("日志"))
        self.tab_Widget.addTab(self.log_Edit,self.m_Parent.tr("日志"))

        layout_Vertical_Top=QHBoxLayout()
        layout_Vertical_Bottom=QHBoxLayout()

        self.tableWidget=QTableWidget(self.m_Parent)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.cellClicked.connect(partial(self.TableCellClicked,"table_click_grid"))

        layout_right=QVBoxLayout()
        layout_Vertical_Top.addWidget(self.tableWidget)
        layout_Vertical_Top.addLayout(layout_right)
        layout_Vertical_Top.setStretchFactor(self.tableWidget,19)
        layout_Vertical_Top.setStretchFactor(layout_right,1)

        layout_h1=QHBoxLayout()
        layout_h2=QHBoxLayout()
        layout_h3=QHBoxLayout()

        label1=QLabel(self.m_Parent.tr("长："))
        label2=QLabel(self.m_Parent.tr("宽："))
        label1.setFont(QFont('微软雅黑',10))
        label2.setFont(QFont('微软雅黑',10))

        combo1=QComboBox(self.m_Parent)
        combo2=QComboBox(self.m_Parent)

        sizeList=SizeSelectList
        self.m_RowCnt=self.m_ColCnt=sizeList[0]
        self.m_ComboRow=combo1
        self.m_ComboCol=combo2
        for obj in (combo1,combo2):
            obj.setCurrentIndex(0)
            for value in sizeList:
                obj.addItem(self.m_Parent.tr("%s"%value))
        self.ResetTableGridSize(self.m_RowCnt,self.m_ColCnt)

        combo1.activated.connect(partial(self.OnComboActivated,"size_select1"))
        combo2.activated.connect(partial(self.OnComboActivated,"size_select2"))

        layout_h1.addWidget(label1)
        layout_h1.addWidget(combo1)
        layout_h2.addWidget(label2)
        layout_h2.addWidget(combo2)

        layout_right.addLayout(layout_h1)
        layout_right.addLayout(layout_h2)

        label_title=QLabel(self.m_Parent.tr("颜色与权重"))

        layout_right.addStretch(1)
        layout_right.addWidget(label_title)

        idx=0
        self.m_CurSelectColor=idx
        sList=GridColorList
        doorLst=SpecialColors[:]
        sList.extend( doorLst )
        for sColor in sList:
            self.m_Parent.m_Grid.SetColorValue(idx, sColor)
            self.m_Parent.m_Grid.SetColorCost(idx, 1)
            if sColor in doorLst:
                if sColor==ColorEnter:
                    sName="入口"
                    self.m_EntranceColor=idx
                elif sColor==ColorExit:
                    sName="出口"
                    self.m_ExitColor=idx
                elif sColor==ColorBlock:
                    sName="障碍物"
                    self.m_BlockColor=idx

                oLabel=QLabel(self.m_Parent.tr("%s"%sName))
                oLabel.setFont(QFont('微软雅黑',10))
                oLabel.setAlignment(QtCore.Qt.AlignCenter)
            else:
                sName="%s"%idx
                oLabel=QLineEdit()
                oLabel.textChanged.connect( partial(self.OnLineColorChanged,idx) )
                oLabel.setText("1")

            oButton=QPushButton(self.m_Parent.tr(""))
            oButton.setStyleSheet('QWidget {background-color:%s}'%sColor)
            func=partial(self.OnButtonClicked,"Color_Label",idx)
            oButton.clicked.connect(func)

            idx+=1

            layout=QHBoxLayout()
            layout.addWidget(oButton)
            layout.addWidget(oLabel)
            layout.setStretchFactor(oButton,2)
            layout.setStretchFactor(oLabel,1)
            layout.addStretch(1)

            layout_right.addLayout(layout)

        layout_right.addStretch(1)
        oLabel1=QLabel(self.m_Parent.tr("当前所选颜色："))
        oLabel1.setFont(QFont('微软雅黑',10))
        self.curColorLabel=QLabel(self.m_Parent.tr(""))
        layout=QHBoxLayout()
        layout.addWidget(self.curColorLabel)
        layout.setStretchFactor(self.curColorLabel,1)
        layout.addStretch(1)

        layout_right.addWidget(oLabel1)
        layout_right.addLayout(layout)

        oButton=QPushButton(self.m_Parent.tr("批量对鼠标所选区块上色"))
        func=partial(self.OnButtonClicked,"Set_Color")
        oButton.clicked.connect(func)
        layout_right.addWidget(oButton)

        layout_right.addStretch(1)
        oButton3=QPushButton(self.m_Parent.tr("开始绘图"))
        oButton3.clicked.connect(partial(self.OnButtonClicked,"Painting"))
        oButton4=QPushButton(self.m_Parent.tr("重置"))
        oButton4.clicked.connect(partial(self.OnButtonClicked,"ResetTable"))
        layout_right.addStretch(1)
        layout_right.addWidget(oButton3)
        layout_right.addWidget(oButton4)
        layout_right.setStretchFactor(oButton3,1)
        layout_right.setStretchFactor(oButton4,1)
        layout_right.addStretch(8)

        self.label_File=QLabel(self.m_Parent.tr(""))
        layout_Vertical_Bottom.addWidget(self.label_File)
        layout_Vertical_Bottom.setStretchFactor(self.label_File,9)
        layout_Vertical_Bottom.addStretch(8)

        graphLayout.addLayout(layout_Vertical_Top)
        graphLayout.addLayout(layout_Vertical_Bottom)
        graphLayout.setStretchFactor(layout_Vertical_Top,9)
        graphLayout.setStretchFactor(layout_Vertical_Bottom,1)

    def ResetTableGridSize(self,iTotalRow,iTotalCol):
        self.m_RowCnt=iTotalRow
        self.m_ColCnt=iTotalCol

        self.tableWidget.clear()
        self.tableWidget.setColumnCount(iTotalCol)
        self.tableWidget.setRowCount(iTotalRow)

        self.m_ComboRow.setCurrentIndex(SizeSelectList.index(iTotalRow))
        self.m_ComboCol.setCurrentIndex(SizeSelectList.index(iTotalCol))

        iRowSize=iColSize=20
        for col in range(iTotalCol):
            self.tableWidget.setColumnWidth(col,iColSize)
        for row in range(iTotalRow):
            self.tableWidget.setRowHeight(row,iRowSize)
        self.m_Parent.m_Grid.ResetAllGrid(iTotalRow,iTotalCol)
        #self.tableWidget.verticalHeader().setVisible(False)
        #self.tableWidget.horizontalHeader().setVisible(False)

    def TableCellClicked(self,sFlag,row,column):
        print("TableCellClicked  ",sFlag,row,column)
        self.SetTableCellColor(row,column,int(self.m_CurSelectColor))

    def SetTableCellColor(self,row,column,idx):
        pos=(row,column)
        if idx==self.m_EntranceColor:
            if self.m_Parent.m_Grid.m_PosEntrance and pos!=self.m_Parent.m_Grid.m_PosEntrance:
                i,j=self.m_Parent.m_Grid.m_PosEntrance
                self.SetTableCellColor(i,j,ColorEmptyIdx)
        if idx==self.m_ExitColor:
            if self.m_Parent.m_Grid.m_PosExport and pos!=self.m_Parent.m_Grid.m_PosExport:
                i,j=self.m_Parent.m_Grid.m_PosExport
                self.SetTableCellColor(i,j,ColorEmptyIdx)

        if not self.m_Parent.m_Grid.SetPosColor((row,column),idx):
            QMessageBox.information(self.m_Parent,"",self.m_Parent.tr("设置颜色失败"))
            return 0

        sColor=self.m_Parent.m_Grid.GetColorValue(idx)
        print("选择了颜色： %s "%str(sColor))
        owidget=QWidget()
        owidget.setStyleSheet('QWidget {background-color:%s}'%sColor)
        self.tableWidget.setCellWidget(row,column,owidget)
        return 1

    def OnLineColorChanged(self,idx,sText):
        print("OnLineColorChanged ",idx,sText)

        sText=sText.strip(" ")
        sText=sText.strip("\t")
        sText=sText.strip("\n")
        if not sText.isdigit():
            sCode="必须输入整数， 当前 输入: %s"%(sText)
            QMessageBox.information(self.m_Parent,"",self.m_Parent.tr(sCode))
            return
        sColor=self.m_Parent.m_Grid.GetColorValue(idx)
        self.m_Parent.m_Grid.SetColorCost(idx, int(sText))

    def OnButtonClicked(self,sFlag,*param):
        print("OnButtonClicked ",sFlag,param)
        if sFlag=="Color_Label":
            idx=int(param[0])
            if idx==self.m_CurSelectColor:
                return
            sColor=self.m_Parent.m_Grid.GetColorValue(idx)
            self.m_CurSelectColor=idx
            self.curColorLabel.setStyleSheet('QWidget {background-color:%s}'%sColor)
        elif sFlag=="Set_Color":
            #oItems=self.tableWidget.selectedItems()
            oList=self.tableWidget.selectedIndexes()
            if len(oList)>=400:
                sCode="一次性批量上色最多只能选择20*20 个"
                QMessageBox.information(self.m_Parent,"",self.m_Parent.tr(sCode))
                return
            for oIndex in oList:
                    row,column=oIndex.row(),oIndex.column()
                    if not self.SetTableCellColor(row,column,self.m_CurSelectColor):
                        break
        elif sFlag=="Painting":
            self.m_Parent.StartPainting()
        elif sFlag=="ResetTable":
            self.tableWidget.clear()
            self.ResetTableGridSize(self.m_RowCnt,self.m_ColCnt)

    def OnComboActivated(self,sFlag,sValue):
        sValue=str(sValue)
        print("OnComboActivated",sFlag,sValue)
        if sFlag=="size_select1":
            idx=int(sValue)
            iRow=SizeSelectList[idx]
            self.ResetTableGridSize(iRow,self.m_ColCnt)
        elif sFlag=="size_select2":
            idx=int(sValue)
            iCol=SizeSelectList[idx]
            self.ResetTableGridSize(self.m_RowCnt,iCol)

    def StatusBarInit(self):
        menubar=self.m_Parent.menuBar()
        fileMenu=menubar.addMenu(self.m_Parent.tr("文件"))
        helpMenu=menubar.addMenu(self.m_Parent.tr("帮助"))

        self.m_Parent.statusBar()

        #QAction是关于菜单栏、工具栏或自定义快捷键动作的抽象。
        exitAction=QAction(QIcon(""),self.m_Parent.tr("退出"),self.m_Parent)
        #定义快捷键。
        exitAction.setShortcut("Ctrl+Q")
        #当鼠标停留在菜单上时，在状态栏显示该菜单的相关信息。
        exitAction.setStatusTip(self.m_Parent.tr("Ctrl+Q 退出程序"))
        #选定特定的动作，发出触发信号。该信号与QApplication部件的quit()方法
        #相关联，这将会终止应用程序。
        exitAction.triggered.connect(qApp.quit)

        importAction=QAction(QIcon(""),self.m_Parent.tr("导入文件"),self.m_Parent)
        importAction.setShortcut("Ctrl+I")
        importAction.setStatusTip(self.m_Parent.tr("Ctrl+I 导入文件程序"))
        importAction.triggered.connect(self.m_Parent.ImportTxtFile)

        exportAction=QAction(QIcon(""),self.m_Parent.tr("保存文件"),self.m_Parent)
        exportAction.setShortcut("Ctrl+S")
        exportAction.setStatusTip(self.m_Parent.tr("Ctrl+S 保存文件"))
        exportAction.triggered.connect(self.m_Parent.ExportToTxtFile)

        fileMenu.addAction(exitAction)
        fileMenu.addAction(importAction)
        fileMenu.addAction(exportAction)

        helpAction=QAction(QIcon(""),self.m_Parent.tr("说明"),self.m_Parent)
        helpAction.setShortcut("Ctrl+H")
        helpAction.setStatusTip(self.m_Parent.tr("弹出帮助窗口"))
        helpAction.triggered.connect(self.m_Parent.OpenHelpWindow)

        aboutAction=QAction(QIcon(""),self.m_Parent.tr("关于"),self.m_Parent)
        aboutAction.setStatusTip(self.m_Parent.tr("程序版本和作者信息"))
        aboutAction.triggered.connect(self.m_Parent.OpenAboutWindow)

        helpMenu.addAction(helpAction)
        helpMenu.addAction(aboutAction)

        toolBar=self.m_Parent.addToolBar(self.m_Parent.tr(""))
        toolBar.addAction(exitAction)
        toolBar.addAction(importAction)
        toolBar.addAction(exportAction)


def start():
    init_runpath()

    try:
        app = QtWidgets.QApplication([])
        window = CApp()
        window.show()
        app.installEventFilter(window)
    except Exception as err:
        print(err)
        debug_print()
    finally:
        sys.exit(app.exec_())

if __name__ == "__main__":
    start()
