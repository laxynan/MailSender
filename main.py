# -*- coding: utf-8 -*-

import Tkinter as tk
import tkMessageBox
import tkFileDialog

import sendMail

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bd=2)
        self.attachments = ()
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.fileButton = tk.Button(self, text='开始发送', command=self.startSend)
        self.fileButton.grid(row=0, column=0)
        self.stateLabel = tk.Label(self, text='')
        self.stateLabel.grid(row=0, column=1, columnspan=3, sticky=tk.W)

        self.fromLabel = tk.Label(self, text='发件人：')
        self.fromLabel.grid(row=1, column=0)
        self.fromInput = tk.Entry(self)
        self.fromInput.grid(row=1, column=1, sticky=tk.W+tk.E)

        self.serverLabel = tk.Label(self, text='SMTP服务器：')
        self.serverLabel.grid(row=1, column=2)
        self.serverInput = tk.Entry(self)
        self.serverInput.grid(row=1, column=3, sticky=tk.W+tk.E)

        self.passwordLabel = tk.Label(self, text='密码：')
        self.passwordLabel.grid(row=2, column=0)
        self.passwordInput = tk.Entry(self, show='*')
        self.passwordInput.grid(row=2, column=1, sticky=tk.W+tk.E)

        self.toLabel = tk.Label(self, text='收件人：')
        self.toLabel.grid(row=3, column=0)
        self.toInput = tk.Entry(self)
        self.toInput.grid(row=3, column=1, sticky=tk.W+tk.E)

        self.titleLabel = tk.Label(self, text='标题：')
        self.titleLabel.grid(row=4, column=0)
        self.titleInput = tk.Entry(self)
        self.titleInput.grid(row=4, column=1, columnspan=3, sticky=tk.W+tk.E)

        self.contentLabel = tk.Label(self, text='正文：')
        self.contentLabel.grid(row=5, column=0)
        self.contentText = tk.Text(self, bg='#eeeeee')
        self.contentText.grid(row=5, column=1, columnspan=3)

        self.attachLabel = tk.Label(self, text='附件：')
        self.attachLabel.grid(row=6, column=0)
        self.fileButton = tk.Button(self, text='添加附件', command=self.chooseFile)
        self.fileButton.grid(row=6, column=1, sticky=tk.W)

    def hello(self):
        name = self.nameInput.get() or 'world'
        tkMessageBox.showinfo('Message', 'Hello, %s' % name)

    def chooseFile(self):
        # filename = tkFileDialog.askopenfilename()
        # print filename
        # fileLabel = Label(self, text=filename)
        # fileLabel.grid()
        filenames = tkFileDialog.askopenfilenames()
        print filenames
        if filenames:
            self.attachments = filenames

    def startSend(self):
        from_addr = self.fromInput.get()
        password = self.passwordInput.get()
        smtp_server = self.serverInput.get()
        to_addr = self.toInput.get()

        title = self.titleInput.get()
        content = self.contentText.get('1.0', tk.END)

        sendMail.startSend(from_addr, password, smtp_server, to_addr, title, content, self.attachments, self.callback)

    def callback(self, sendState, successNum, failedNum):
        if sendState == 1:
            self.stateLabel['text'] = '已发送'
        else:
            self.stateLabel['text'] = '发送中...'


app = Application()
# 设置窗口标题:
app.master.title('Send Mail')
# 主消息循环:
app.mainloop()