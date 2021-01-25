import sys
sys.path.append('..\\')
sys.path.append('..\\NLP')

from tkinter import *
from iniconfig import iniconfig
from NLP.db_occur_equiz import db_occur_equiz
from tkinter import messagebox

class LR_hazardsuj_buttons():



    #def __init__(self, root,dbcursor,textpad):
    def __init__(self, root,textpad):
        self.iniconfig = iniconfig()
        self.root = root
        self.textpad = textpad
        # self.dbcursor = dbcursor
        # self.textpad = textpad
        if __name__ == '__main__':
            hazard_sub = PhotoImage(file='../temp/hazard_sub.gif')
            add_inchain = PhotoImage(file='../temp/add_inchain.gif')
        else:
            hazard_sub = PhotoImage(file='./temp/hazard_sub.gif')
            add_inchain = PhotoImage(file='./temp/add_inchain.gif')

        # Btn_next = Button(root, text="Next",image=im_right,command = self._db_next)
        # Btn_pre = Button(root, text="Pre",image=im_left,command = self._db_pre)
        #Btn_next = Button(root, text="Next",image=im_right)
        Btn_del = Button(root, text="Delete",width = 15, command = self._del_occur_incollection)
        Btn_add = Button(root, text="Add",width = 15, command = self._add_hazard_sub_incollection)

        img_lbl_del = Label(root, image=hazard_sub)
        img_lbl_add = Label(root, image=add_inchain)
        img_lbl_del.image = hazard_sub
        #img_lbl_add.image = add_inchain

        Btn_del.grid(row=1, column=0,padx=30,pady=3)
        Btn_add.grid(row=1, column=2,padx=30,pady=3)

        img_lbl_del.grid(row=0, column=1,padx=1,pady=3)
        #img_lbl_add.grid(row=0, column=1,padx=1,pady=3)



    def _del_occur_incollection(self):
        return
        # 不物理删除，只是把inchain变成false
        # if self.textpad.isfocus:
        #     db = db_occur_equiz(self.textpad.dbcursor)
        #     db.del_oneoccur(self.textpad.focus_index)
        #     self.textpad.Connect_External_Module_Features()

    def _add_hazard_sub_incollection(self):
        if self.textpad.tag_ranges("sel"): #判断是否有文本被选中
            dic_hazard_sub={}
            dic_hazard_sub['str_begin'] = int(str(self.textpad.index("sel.first"))[2:])
            dic_hazard_sub['str_end'] = int(str(self.textpad.index("sel.last"))[2:])
            dic_hazard_sub['text'] = self.textpad.get(self.textpad.index("sel.first"),self.textpad.index("sel.last"))
            db = db_occur_equiz(self.textpad.dbcursor)
            db.create_new_hazard_sub(dic_hazard_sub,self.textpad.occur_clickindex)
            self.textpad.Connect_External_Module_Features()







if __name__ == '__main__':
        root = Tk()
        #model_buttons(root)

        root.mainloop()