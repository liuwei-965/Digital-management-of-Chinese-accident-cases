import sys
sys.path.append('.\GUI')
sys.path.append('..\\NLP')

from NLP.db_occur_equiz import db_occur_equiz
import tkinter

class RenderText():

    def __init__(self, text,dbcursor,db):
        self.text = text
        self.db = db_occur_equiz(dbcursor)
        self.obj_id = self.db.getcurrent_objid()
        #print(self.obj_id)
        dic_db = self.db.getOneCase(self.obj_id)
        self.render(dic_db)
        self.get_objid(self.db.get_case_collection())


    def render(self, db_dic):
        self.text.delete('1.0', 'end')
        self.text.insert("1.0", db_dic['transversion'])
        #lst_occur = self.db.has_occur
        i = 0
        for x in db_dic:
            if 'occur' in x:
                if db_dic[x]["inChain"]:
                    #print(db_dic[x]['text'])
                    tagbegin = "{}.{}".format(1, db_dic[x]["str_begin"])
                    tagend = "{}.{}".format(1, db_dic[x]["str_end"])
                    #print(coordinates)
                    if i%2 == 0:
                        self.text.tag_add("occur1", tagbegin, tagend)
                    else:
                        self.text.tag_add("occur2", tagbegin, tagend)

                    i = i+1

            self.text.tag_configure("occur1", background="skyblue", foreground="red", relief='raised',
                                    borderwidth=1)
            self.text.tag_configure("occur2", background="skyblue", foreground="red")


            #self.text.tag_configure("occur", underline=True, lmargin1=2 )
    def get_objid(self,db_dic):
        return db_dic['_id']


if __name__ == '__main__':
    root = tkinter.Tk()
    pad = tkinter.Text(root)
    pad.pack()
    RenderText(pad,6)
    root.mainloop()