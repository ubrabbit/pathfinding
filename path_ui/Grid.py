#coding: utf-8

import sys
import copy
import math
import re

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QMessageBox


from Common import *


class CGrid(object):

    m_ReFindSize=re.compile("\$size\((\d+),(\d+)\)")
    m_ReFineVersion=re.compile("\$version\((.+)\)")

    m_EnterFlag="${Enter}"
    m_ExitFlag="${Exit}"
    m_BlockFlag="${Block}"

    def __init__(self,parent):
        self.m_Parent=parent

        self.m_Row=0
        self.m_Col=0
        self.m_PosEntrance=()
        self.m_PosExport=()
        self.m_BlockList=[]

        self.m_PosColors={}

        self.m_ColorValues = {}
        self.m_ColorCosts = {}

    def ResetAllGrid(self,iTotalRow,iTotalCol):
        self.m_Row=iTotalRow
        self.m_Col=iTotalCol

        self.m_PosEntrance=()
        self.m_PosExport=()

        self.m_PosColors={}
        self.m_BlockList=[]
        for pos in [(i,j) for i in range(iTotalRow) for j in range(iTotalCol)]:
            self.m_PosColors[pos]=0

    def SetPosColor(self,pos,color):
        if pos==self.m_PosEntrance:
            self.m_PosEntrance=()
        if pos==self.m_PosExport:
            self.m_PosExport=()
        if pos in self.m_BlockList:
            self.m_BlockList.remove(pos)

        self.m_PosColors[pos]=color
        if color==self.m_Parent.m_Interface.m_EntranceColor:
            self.m_PosEntrance=pos
        if color==self.m_Parent.m_Interface.m_ExitColor:
            self.m_PosExport=pos
        if color==self.m_Parent.m_Interface.m_BlockColor:
            if not pos in self.m_BlockList:
                self.m_BlockList.append( pos )
        else:
            if pos in self.m_BlockList:
                self.m_BlockList.remove( pos )
        return 1

    def GetPosColor(self,pos):
        return self.m_PosColors[pos]

    def SetColorCost(self,color,cost=1):
        self.m_ColorCosts[ color ] = cost

    def SetColorValue(self,color,value):
        self.m_ColorValues[ color ] = value

    def GetColorValue(self,color):
        assert(color in self.m_ColorValues)
        return self.m_ColorValues[color]

    def GetPosList(self):
        posList = []
        for pos in [(i,j) for i in range(self.m_Row) for j in range(self.m_Col)]:
            color = self.m_PosColors[pos]
            x, y = pos
            cost = self.m_ColorCosts[ color ]
            posList.append( (x,y,cost) )
        return posList

    def GetBlockList(self):
        return self.m_BlockList[:]

    def ValidPaint(self):
        print("self.m_ColorCosts   ",self.m_ColorCosts)
        print("self.m_ColorValues   ",self.m_ColorValues)
        if len(self.m_ColorCosts) != len(self.m_ColorValues):
            return "颜色权重未完全输入"
        return ""

    def SaveTxt(self):
        sFile=\
"""$version(%s)
$size(%s,%s)
%s
"""
        sContent=[]
        for i in range(self.m_Row):
            sList=[]
            for j in range(self.m_Col):
                pos=(i,j)
                if pos==self.m_PosEntrance:
                    sKey=self.m_EnterFlag
                elif pos==self.m_PosExport:
                    sKey=self.m_ExitFlag
                elif pos in self.m_BlockList:
                    sKey=self.m_BlockFlag
                else:
                    iColor=self.m_PosColors.get(pos,0)
                    sKey="%s"%iColor
                sList.append(sKey)
            sContent.append( " ".join(sList) )
        sFile=sFile%(VERSION,self.m_Row,self.m_Col,"\n".join(sContent))

        print("SaveTxt ",sFile)
        return sFile

    def LoadTxt(self,sFile):
        sFile=sFile.strip("\t")
        sFile=sFile.strip(" ")
        sCodeLst=sFile.split("\n")
        sHead=""
        while(sHead==""):
            sHead=sCodeLst.pop(0)

        oGroup=self.m_ReFineVersion.match(sHead)
        if not oGroup or oGroup.group(1).strip(" ")!="%s"%VERSION:
            QMessageBox.information(self.m_Parent,"导入错误",self.m_Parent.tr("文件版本已经不一致"))
            return 0,0,{}

        sHead=sCodeLst.pop(0)
        oGroup=self.m_ReFindSize.match(sHead)
        iRow,iCol=int(oGroup.group(1)),int(oGroup.group(2))
        dPos={}
        for i in range(iRow):
            sList=sCodeLst.pop(0)
            sList=sList.split(" ")
            for j in range(iCol):
                pos=(i,j)
                if sList:
                    sKey=sList.pop(0)
                    if sKey==self.m_EnterFlag:
                        idx=self.m_Parent.m_Interface.m_EntranceColor
                    elif sKey==self.m_ExitFlag:
                        idx=self.m_Parent.m_Interface.m_ExitColor
                    elif sKey==self.m_BlockFlag:
                        idx=self.m_Parent.m_Interface.m_BlockColor
                    else:
                        idx=int(sKey)
                    iColor=idx
                else:
                    iColor=0
                dPos[pos]=iColor
        return iRow,iCol,dPos
