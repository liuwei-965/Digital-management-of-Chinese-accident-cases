import sys
sys.path.append('.\GUI')
sys.path.append('.\\NLP')

from tkinter import *
from iniconfig import iniconfig
from NLP.db_occur_equiz import db_occur_equiz 

class browser_ButtonGroup():

    def __init__(self,dbnlp, root,dbcursor,textpad):
        self.iniconfig = iniconfig()
        self.root = root
        self.dbcursor = dbcursor   #游标
        self.textpad = textpad
        self.db = db_occur_equiz(dbcursor)
        if __name__ == '__main__':
            im_left = PhotoImage(file='../temp/left.gif')
            im_right = PhotoImage(file='../temp/right.gif')
        else:
            im_left = PhotoImage(file='./temp/left.gif')
            im_right = PhotoImage(file='./temp/right.gif')

        Btn_next = Button(root, text="Next",image=im_right,command = self._db_next)
        Btn_pre = Button(root, text="Pre",image=im_left,command = self._db_pre)
        Btn_upload = Button(root, text="Up occur", command=self._upload_occur)
        Btn_next.image = im_right
        Btn_pre.image = im_left

        Btn_pre.grid(row=0, column=0,padx=1,pady=3)
        Btn_next.grid(row=0, column=1,padx=1,pady=3)
        Btn_upload.grid(row=0, column=7,padx=1,pady=3)

        Label(root, text=" ").grid(row=0, column=2, sticky=E,padx=50,pady=3)
        Label(root, text="Case No.").grid(row=0, column=3, sticky=E,padx=5,pady=3)
        self.e = StringVar()
        Entry(root,width = 5,textvariable=self.e).grid(row=0, column=4,padx=5,pady=3)    #显示页码
        self.e.set(str(dbcursor+1))
        #self.e.set(str(dbcursor))
        Label(root, text= self.db.case_num).grid(row=0, column=5, sticky=W, padx=2, pady=3)
        Button(root, text="Send").grid(row=0, column=6,padx=1,pady=3)

    def _db_next(self):
        #print("当前dbcursor %s" %self.dbcursor)
        if self.dbcursor < self.db.case_num-1:
        #while self.dbcursor < self.db.case_num - 1:  #用于初始批量标准化MongoDB数据
            #print(self.dbcursor)
            self.dbcursor = self.dbcursor+1
            #print("next1后 dbcursor %s" % self.dbcursor)
            #self._occur_nlp(self.dbcursor)    #对当前案例进行自然语言处理，并匹配动词  初始批量标准化
            self.textpad.dbcursor = self.dbcursor
            self.textpad.Connect_External_Module_Features()
        else:
            self.dbcursor = 0
            #print("next2后 dbcursor %s" % self.dbcursor)
            #self._occur_nlp(self.dbcursor)   #初始批量标准化
            self.textpad.dbcursor = self.dbcursor
            self.textpad.Connect_External_Module_Features()
        self.iniconfig.set_dbcursor(self.dbcursor+1)   #保存本次页码
        self.e.set(str(self.dbcursor+1))  #更新窗口页码
        #self.e.set(str(self.dbcursor))  # 更新窗口页码

    def _db_pre(self):
        '''向前按钮'''
        #print("当前dbcursor %s" % self.dbcursor)
        if self.dbcursor>0:
            self.dbcursor = self.dbcursor-1
            #print("pre1后 dbcursor %s" % self.dbcursor)
            #self._occur_nlp(self.dbcursor)   #初始批量标准化
            self.textpad.dbcursor = self.dbcursor
            self.textpad.Connect_External_Module_Features()
        else:
            self.dbcursor = self.db.case_num-1
            #print("pre2后 dbcursor %s" % self.dbcursor)
            #self._occur_nlp(self.dbcursor)   #初始批量标准化
            self.textpad.dbcursor = self.dbcursor
            self.textpad.Connect_External_Module_Features()
        self.iniconfig.set_dbcursor(self.dbcursor+1)
        self.e.set(str(self.dbcursor+1))


    def _occur_nlp(self, dbcursor):
         '''对当前案例文本进行自然语言处理，并将动词在案例中出现的情况记录在案例库中'''
         db = db_occur_equiz(self.dbcursor)   #实例化 类db_occur_equiz
         db.getOneCase(db.getcurrent_objid())    #获取当前id的案例记录
         db._find_occur()  #对当前案例文本进行自然语言处理，并将动词在案例中出现的情况记录在案例库中

    def _upload_occur(self):
        '''将链中的动词添加到动词库中'''
        db = db_occur_equiz(self.dbcursor)
        db.getOneCase(db.getcurrent_objid())
        db.upload_occur_2tag()   #将链中的动词添加到动词库中


if __name__ == '__main__':
        root = Tk()
        #ButtonGroup(root)
        browser_ButtonGroup(root)
        root.mainloop()