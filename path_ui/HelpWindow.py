# -*- coding: utf-8 -*-

"""
帮助窗口实现，同时也是堆栈窗口的范例
"""

import sys

from PyQt5 import QtCore, QtGui, QtWidgets


#显示中文
QtCore.QTextCodec.setCodecForLocale(QtCore.QTextCodec.codecForName("system"))

g_Help={
    "帮助窗口":\
"""
呵呵哒
""",
}


def GetHelp(sKey):
    return g_Help.get(sKey,"")


class CHelpDialog(QtWidgets.QDialog):


    def __init__(self,parent=None):
        super(CHelpDialog,self).__init__(parent)

        self.setWindowTitle(self.tr("帮助窗口"))

        self.listWidget=QtWidgets.QListWidget()
        oStack=QtWidgets.QStackedWidget()

        for idx,sKey in enumerate(g_Help.keys()):

            self.listWidget.insertItem(idx,self.tr(sKey))
            label=QtWidgets.QLabel(self.tr(GetHelp(sKey)))
            oStack.addWidget(label)


        mainLayout=QtWidgets.QHBoxLayout(self)

        mainLayout.addWidget(self.listWidget)
        mainLayout.addWidget(oStack)

        #设置布局空间的比例
        mainLayout.setStretchFactor(self.listWidget,1)
        mainLayout.setStretchFactor(oStack,3)

        #连接 QListWidget 的 currentRowChanged()信号与堆栈窗的 setCurrentIndex()槽，
        #实现按选择显示窗体。 此处的堆栈窗体 index 按插入的顺序从 0 起依次排序， 与 QListWidget
        #的条目排序相一致
        self.listWidget.currentRowChanged.connect( oStack.setCurrentIndex )


def Open():
    window=CHelpDialog()
    return window


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window=Open()
    window.show()
    sys.exit(app.exec_())
