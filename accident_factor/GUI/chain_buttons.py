import sys
sys.path.append('..\\')
sys.path.append('..\\NLP')

from tkinter import *
from iniconfig import iniconfig
from NLP.db_occur_equiz import db_occur_equiz
from GUI.model_buttons import model_buttons
from tkinter import messagebox

class chain_buttons():
    #def __init__(self, root,dbcursor,textpad):
    def __init__(self, root,textpad):
        self.iniconfig = iniconfig()
        self.root = root
        self.textpad = textpad
        # self.dbcursor = dbcursor
        # self.textpad = textpad
        if __name__ == '__main__':
            del_inchain = PhotoImage(file='../temp/del_inchain.gif')
            add_inchain = PhotoImage(file='../temp/add_inchain.gif')
        else:
            del_inchain = PhotoImage(file='./temp/del_inchain.gif')
            add_inchain = PhotoImage(file='./temp/add_inchain.gif')

        # Btn_next = Button(root, text="Next",image=im_right,command = self._db_next)
        # Btn_pre = Button(root, text="Pre",image=im_left,command = self._db_pre)
        #Btn_next = Button(root, text="Next",image=im_right)
        Btn_del = Button(root, text="Delete",width = 15, command = self._del_occur_incollection)
        Btn_add = Button(root, text="Add",width = 15, command = self._add_occur_incollection)

        img_lbl_del = Label(root, image=del_inchain)
        img_lbl_add = Label(root, image=add_inchain)
        img_lbl_del.image = del_inchain
        img_lbl_add.image = add_inchain

        Btn_del.grid(row=1, column=0,padx=30,pady=3)
        Btn_add.grid(row=1, column=1,padx=30,pady=3)

        img_lbl_del.grid(row=0, column=0,padx=1,pady=3)
        img_lbl_add.grid(row=0, column=1,padx=1,pady=3)



    # def _del_occur_incollection(self): #NI
    #     #不物理删除，只是把inchain变成false
    #     #print('%s 你已选中索引' %self.textpad.focus_index)
    #     if self.textpad.isfocus:
    #         db = db_occur_equiz(self.textpad.dbcursor)
    #         db.del_oneoccur(self.textpad.focus_index)
    #         #db.del_oneoccur(int(str(self.textpad.index("sel.first"))[2:]),int(str(self.textpad.index("sel.last"))[2:]))
    #         #print('%d 你已选中索引' % (int(str(self.textpad.index("sel.first"))[2:]),int(str(self.textpad.index("sel.last"))[2:])))
    #         self.textpad.Connect_External_Module_Features()

    def _del_occur_incollection(self):
        #不物理删除，只是把inchain变成false
        #print('%s 你已选中索引' %self.textpad.focus_index)
        db = db_occur_equiz(self.textpad.dbcursor)
        #db.del_oneoccur(self.textpad.focus_index)
        db.del_oneoccur(int(str(self.textpad.index("sel.first"))[2:]),int(str(self.textpad.index("sel.last"))[2:]))
        #print('%s 你已选中索引' % ((str(self.textpad.index("sel.first"))[2:]),(str(self.textpad.index("sel.last"))[2:])))
        self.textpad.Connect_External_Module_Features()

    def _add_occur_incollection(self):
        '''创建新的occur'''
        dic_occur={}
        dic_occur['str_begin'] = int(str(self.textpad.index("sel.first"))[2:])   #添加词的开始索引
        #print('hhh:%s'%(self.textpad.index("sel.first"))[2:])
        dic_occur['str_end'] = int(str(self.textpad.index("sel.last"))[2:])     #添加词的结束索引
        #print('hhh:%s' % (self.textpad.index("sel.last"))[2:])
        dic_occur['text'] = self.textpad.get(self.textpad.index("sel.first"),self.textpad.index("sel.last"))
        print(dic_occur)
        db = db_occur_equiz(self.textpad.dbcursor)
        db.create_new_occur(dic_occur)
        self.textpad.Connect_External_Module_Features()


if __name__ == '__main__':
        root = Tk()
        model_buttons(root)

        root.mainloop()