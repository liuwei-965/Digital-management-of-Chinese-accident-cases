import threading
from gensim.models.phrases import Phrases, Phraser
import logging
from tkinter import *
import jieba.posseg as pseg
from NLP.db_occur_equiz import db_occur_equiz

class phase_thread (threading.Thread):
    def __init__(self, phaseframe,threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        self.phaseframe = phaseframe
        self.hasload = False
        self.lbl_var = StringVar()
        self.lbl_var.set('Phase file is loading...')
        Label(self.phaseframe, textvariable = self.lbl_var).grid(row=1, column=0, padx=1,pady=3)

    def run(self):
        self.load_phase_file()
        return

    def load_phase_file(self):
        phrases = Phrases().load('.\\temp\phase_risknet_description')
        self.bigram = Phraser(phrases)
        self.lbl_var.set('Phase module is ready')
        self.hasload = True

    def get_twoside_phase_score(self,dbcursor,click_index):
        list_raw_word = [] #分词数列
        list_raw_tag = [] #词性标注数列
        db = db_occur_equiz(dbcursor)
        obj_id = db.getcurrent_objid()
        dic_case = db.getOneCase(obj_id)
        if self.hasload:
            #print(click_index)
            words = pseg.cut(dic_case['transversion'])
            for word, flag in words:
                list_raw_word.append(word)
                list_raw_tag.append(flag)
            left = 0
            right = 0
            i=0
            while i<len(list_raw_word)-1:
                left=len(list_raw_word[i])+left
                right = left+len(list_raw_word[i+1])
                if left<=click_index and right>=click_index:
                    str_click = list_raw_word[i+1]
                    str_left = list_raw_word[i]
                    str_right = list_raw_word[i+2]
                    # print('='*20)
                    # print(list_raw_tag[i]+'  '+list_raw_word[i+1])
                    # print(list_raw_tag[i+1]+'  '+list_raw_word[i])
                    # print(list_raw_tag[i+2]+'  '+list_raw_word[i+2])
                    left_lst_com = [str_left.encode(), str_click.encode()]
                    right_lst_com = [str_click.encode(), str_right.encode()]
                    leftscore = self.bigram.score_item(str_left, str_click, left_lst_com, scorer='default')
                    rightscore = self.bigram.score_item(str_click, str_right, right_lst_com, scorer='default')
                    if leftscore>-1:
                        self.lbl_var.set(str_left+' '+str_click+'may be is one word')
                    elif rightscore>-1:
                        self.lbl_var.set(str_click+' '+str_right + 'may be is one word')
                    else:
                        self.lbl_var.set('No phase')
                        print('ok')
                    break
                i = i+1
        else:
            self.lbl_var.set('Phase module is not ready')


    def _two_words_score(self,A,B):
        lst_com = [A.encode(), B.encode()]
        return self.bigram.score_item(u'1', u'2', lst_com, scorer='default')