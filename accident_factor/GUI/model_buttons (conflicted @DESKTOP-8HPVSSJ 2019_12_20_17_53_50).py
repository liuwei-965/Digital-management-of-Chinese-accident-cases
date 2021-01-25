import sys
sys.path.append('..\\')
sys.path.append('..\\NLP')

from tkinter import *
from iniconfig import iniconfig
from NLP.db_occur_equiz import db_occur_equiz
from tkinter import messagebox

class model_buttons():



    def __init__(self, root,dbcursor,textpad):
        self.iniconfig = iniconfig()
        self.root = root
        self.dbcursor = dbcursor
        # self.dbcursor = dbcursor
        self.textpad = textpad
        if __name__ == '__main__':
            del_inchain = PhotoImage(file='../temp/del_inmodel.gif')
            add_inchain = PhotoImage(file='../temp/add_inmodel.gif')
        else:
            del_inchain = PhotoImage(file='./temp/del_inmodel.gif')
            add_inchain = PhotoImage(file='./temp/add_inmodel.gif')

        # Btn_next = Button(root, text="Next",image=im_right,command = self._db_next)
        # Btn_pre = Button(root, text="Pre",image=im_left,command = self._db_pre)
        #Btn_next = Button(root, text="Next",image=im_right)
        Btn_del = Button(root, text="Delete",width = 15, command=self._del)
        Btn_add = Button(root, text="Add",width = 15, command=self._add)

        img_lbl_del = Label(root, image=del_inchain)
        img_lbl_add = Label(root, image=add_inchain)
        img_lbl_del.image = del_inchain
        img_lbl_add.image = add_inchain

        Btn_del.grid(row=1, column=0,padx=25,pady=3)
        Btn_add.grid(row=1, column=2,padx=25,pady=3)

        img_lbl_del.grid(row=0, column=0,padx=1,pady=3)
        img_lbl_add.grid(row=0, column=2,padx=1,pady=3)





    def _occur_nlp(self, dbcursor):
         #m=messagebox.showinfo('info', 'model is upgrading')
         b = db_occur_equiz(dbcursor)
         b.getOneCase(b.getcurrent_objid())
         b.nlp()
    def _del(self):
        if self.textpad.isfocus:
            db = db_occur_equiz(self.textpad.dbcursor)
            db.add_2stopword(self.textpad.focus_index)
            db.nlp()
            self.textpad.Connect_External_Module_Features()

    def _add(self):
        if self.textpad.isfocus:
            db = db_occur_equiz(self.textpad.dbcursor)
            db.add_terminology_dic()





if __name__ == '__main__':
        root = Tk()
        model_buttons(root)

        root.mainloop()