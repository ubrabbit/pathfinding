#coding: utf-8

"""
/*
 *  Copyright (C) 2011-2017 ubrabbit
 *  Author: ubrabbit <ubrabbit@gmail.com>
 *  Date: 2017-01-22 12:46:11
 *
 */

 """

from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial

import sys


def ConsoleInit(window):
    console_Edit=QtWidgets.QTextEdit()
    log_Edit=QtWidgets.QTextEdit()
    console_Edit.setReadOnly(True)
    log_Edit.setReadOnly(True)

    cb_stdout=partial(StdoutOutput,console_Edit)
    cb_stderr=partial(StderrOutput,log_Edit)

    sys.stdout=EmittingStream(textWritten=cb_stdout)
    sys.stderr=EmittingStream(textWritten=cb_stderr)

    return console_Edit,log_Edit

def ConsoleFree():
    sys.stdout=sys.__stdout__
    sys.stderr=sys.__stderr__

#回调不能出现 print ，不然就无限递归了
def StdoutOutput(console_Edit,text):
    cursor=console_Edit.textCursor()
    cursor.movePosition(QtGui.QTextCursor.End)
    cursor.insertText(text)
    console_Edit.setTextCursor(cursor)
    console_Edit.ensureCursorVisible()

def StderrOutput(log_Edit,text):
    cursor=log_Edit.textCursor()
    cursor.movePosition(QtGui.QTextCursor.End)
    cursor.insertText(text)
    log_Edit.setTextCursor(cursor)
    log_Edit.ensureCursorVisible()

class EmittingStream(QtCore.QObject):

    textWritten=QtCore.pyqtSignal(str)

    def write(self,text):
        #emit：发射信号
        self.textWritten.emit(str(text))
