import sys
sys.path.append('.\GUI')
sys.path.append('..\\NLP')

from NLP.db_occur_equiz import db_occur_equiz
import tkinter
import jieba.posseg as pseg

class LR_RenderText():

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
                    tagbegin = "{}.{}".format(1, db_dic[x]["str_begin"])
                    tagend = "{}.{}".format(1, db_dic[x]["str_end"])
                    #print(coordinates)
                    if i%2 == 0:
                        self.text.tag_add("occur1", tagbegin, tagend)
                    else:
                        self.text.tag_add("occur2", tagbegin, tagend)

                    i = i+1

            self.text.tag_configure("occur1", underline=True, lmargin1=2, foreground="blue", relief='raised',
                                    borderwidth=1)
            self.text.tag_configure("occur2", underline=True, lmargin1=2, foreground="blue")

        for x in db_dic:
            if 'hazard_sub' in x:
                if db_dic[x]["inChain"]:
                    tagbegin = "{}.{}".format(1, db_dic[x]["str_begin"])
                    tagend = "{}.{}".format(1, db_dic[x]["str_end"])
                    self.text.tag_add("hazard_sub", tagbegin, tagend)
            if 'atrisk' in x:
                if db_dic[x]["inChain"]:
                    tagbegin = "{}.{}".format(1, db_dic[x]["str_begin"])
                    tagend = "{}.{}".format(1, db_dic[x]["str_end"])
                    self.text.tag_add("atrisk", tagbegin, tagend)

        self.text.tag_configure("hazard_sub", background = 'red', lmargin1=2, foreground="black")
        self.text.tag_configure("atrisk", background = 'cyan', lmargin1=2, foreground="black")




            #self.text.tag_configure("occur", underline=True, lmargin1=2 )
    def focus_one_occur(self, click_index,dbcursor):
        self.text.tag_delete('hazard1')
        self.text.tag_delete('hazard2')
        list_raw_word = [] #分词数列
        list_raw_tag = [] #词性标注数列
        lst_word_left_right = [] #每一个要素是一个二元组，一个是左，一个是右
        #list_include_tag = ['an', 'ad', 'b', 'f', 'j', 'l', 'm', 'n', 'nt', 'nx', 'nz', 's', 'v', 'vg', 'vn', 'q']
        list_include_tag = [ 'n', 'nr', 'nx', 'nz', 'q']
        db = db_occur_equiz(dbcursor)
        obj_id = db.getcurrent_objid()
        dic_case = db.getOneCase(obj_id)
        words = pseg.cut(dic_case['transversion'])
        for word, flag in words:
            list_raw_word.append(word)
            list_raw_tag.append(flag)
        left = 0
        right = 0
        i=0
        while i<len(list_raw_word)-1:
            left=right
            right = left+len(list_raw_word[i])
            lst_word_left_right.append((left, right))
            i = i+1
        j=0
        #定位点击词在整个分词序列中的位置
        while j <= len(lst_word_left_right)-1:
            int_lst_clickindex = len(lst_word_left_right)-1
            if lst_word_left_right[j][0]<=click_index and click_index<=lst_word_left_right[j][1]:
                int_lst_clickindex = j
                #print(list_raw_word[int_lst_clickindex])
                break
            j = j+1
        int_windows = 3
        #标记左侧名词（int_windows个），如果有的话；
        #print(db.get_occur_type(list_raw_word[int_lst_clickindex]))

        i=0
        count = 0
        # ABC三种情况，a往前找，b往后找，c找附近

        if db.get_occur_type(list_raw_word[int_lst_clickindex]) == 'a':
            cursor = int_lst_clickindex - 1
            while cursor>=0:
                if list_raw_tag[cursor] in list_include_tag:
                    if count < int_windows:
                            tagbegin = "{}.{}".format(1,  lst_word_left_right[cursor][0])
                            tagend = "{}.{}".format(1, lst_word_left_right[cursor][1])
                            if count % 2 == 0:
                                self.text.tag_add("hazard1", tagbegin, tagend)
                            else:
                                self.text.tag_add("hazard2", tagbegin, tagend)
                            count = count + 1
                cursor = cursor -1

        if db.get_occur_type(list_raw_word[int_lst_clickindex]) == 'b':
            cursor = int_lst_clickindex + 1
            while cursor < len(lst_word_left_right):
                if list_raw_tag[cursor] in list_include_tag:
                    if count<int_windows:
                        if cursor < len(lst_word_left_right):
                            tagbegin = "{}.{}".format(1, lst_word_left_right[cursor][0])
                            tagend = "{}.{}".format(1, lst_word_left_right[cursor][1])
                            if count % 2 == 0:
                                self.text.tag_add("hazard1", tagbegin, tagend)
                            else:
                                self.text.tag_add("hazard2", tagbegin, tagend)
                        count = count + 1
                cursor = cursor +1

        #print(db.get_occur_type(list_raw_word[int_lst_clickindex]))
        if db.get_occur_type(list_raw_word[int_lst_clickindex]) == 'c':
            left_cursor = int_lst_clickindex - 1
            right_cursor = int_lst_clickindex + 1
            int_right_numer = 10000
            int_left_numer = 10000
            while left_cursor >= 0:
                if list_raw_tag[left_cursor] == 'm':
                    int_left_numer = int_lst_clickindex - left_cursor
                    break
                left_cursor = left_cursor -1
            while right_cursor < len(lst_word_left_right):
                if list_raw_tag[right_cursor] == 'm':
                    int_right_numer = right_cursor - int_lst_clickindex
                    break
                right_cursor = right_cursor+1

            if int_left_numer < int_right_numer:
                tagbegin = "{}.{}".format(1, lst_word_left_right[left_cursor][0])
                tagend = "{}.{}".format(1, lst_word_left_right[left_cursor+1][1])
            else:
                tagbegin = "{}.{}".format(1, lst_word_left_right[right_cursor][0])
                tagend = "{}.{}".format(1, lst_word_left_right[right_cursor+1][1])
            self.text.tag_add("hazard1", tagbegin, tagend)




        self.text.tag_configure("hazard1", background = 'skyblue', lmargin1=2, foreground="red")
        self.text.tag_configure("hazard2", background = 'yellow', lmargin1=2, foreground="grey")

        self.text.tag_bind("hazard1", '<Button-1>', self.text._hazsub_eleATrisk_click)
        self.text.tag_bind("hazard2", '<Button-1>', self.text._hazsub_eleATrisk_click)


        return






    def get_objid(self,db_dic):
        return db_dic['_id']




if __name__ == '__main__':
    root = tkinter.Tk()
    pad = tkinter.Text(root)
    pad.pack()
    RenderText(pad,6)
    root.mainloop()