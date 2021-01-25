import re

from pymongo import MongoClient
from bson.objectid import ObjectId
import jieba
import jieba.posseg as pseg
import tkinter.messagebox

class db_occur_equiz():

    myclient = MongoClient('mongodb://localhost:27017/')
    mydb = myclient["高空坠落事故坠落"]
    test_collection = mydb["fall 200"]
    db_verb_types = mydb["fact_all"]

    obj_id=''
    _rawtext= ''

    def __init__(self,id_cursor, cleardb = False):
        if __name__ == '__main__':
            self.str_dir = '../temp/stopwords.txt'  #当前目录上级目录
            self.userdict = '../temp/userdict.txt'
        else:
            self.str_dir = './temp/stopwords.txt'   #当前目录
            self.userdict = './temp/userdict.txt'
        self.lst_objid = self._get_idlist()
        #print(self.lst_objid)
        self.case_num = len(self.lst_objid)

        if -1<id_cursor< self.case_num:
            self.int_id_cursor = id_cursor
        else:
            self.int_id_cursor = 0
        self.obj_id= self.lst_objid[self.int_id_cursor]   #索引与id 对应

        if cleardb:
            self._cleardb()  #删除字段


    def getcurrent_objid(self):
        '''获取目前id'''
        return  self.obj_id

    def get_case_collection(self):
        lst = self._get_idlist()
        return self.test_collection.find_one({"_id": ObjectId(lst[self.int_id_cursor])})


    def _get_idlist(self):
        '''获取mongodb中数据的id'''
        lst_id = []
        i = 1
        for x in self.test_collection.find({},{"_id":1}):
            lst_id.append(x['_id'])
            #print(x['_id'])
            # print(i)
            # i=i+1
        return lst_id

    #每次进入一个case 重新学习occur
    def add_terminology_dic(self):
        f = open(self.userdict, "a+", encoding='utf-8')
        f.write('流淌火  \n')
        f.close()


    def nlp(self):
        '''TODO 每点因素 对当前案例文本进行自然语言处理，并将动词在案例中出现的情况记录在案例库中'''
        jieba.load_userdict(self.userdict)   #添加自定义词典userdict
        self.stopwords = self._stopwordslist(self.str_dir)  # 加载停留词
        words = pseg.cut(self._rawtext)   #对案例进行切分词
        list_raw_word = [] #分词数列
        list_raw_tag = [] #词性标注数列
        for word, flag in words:
            list_raw_word.append(word)
            list_raw_tag.append(flag)
        self._find_occur(list_raw_word)


    def _stopwordslist(self,filepath):
        '''停用词词典'''
        stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
        return stopwords

    def _cleardb(self):
        '''删除字段'''
        #print('clear db')
        for x in self.get_occur_list():
            self.test_collection.update({"_id": ObjectId(self.obj_id)}, {'$unset': {x: 1}})
        for x in self.has_equiz():
            self.test_collection.update({"_id": ObjectId(self.obj_id)}, {'$unset': {x: 1}})


    def add_newoccur_to_verbtypes(self):
        print('done')

    # def del_oneoccur(self,click_index):
    #     # print(self.int_id_cursor)
    #     # print(click_index)
    #     dic_case = self.getOneCase(self.getcurrent_objid())
    #     for x in dic_case:
    #         if 'occur' in x:
    #             if dic_case[x]['str_begin'] <= click_index and dic_case[x]['str_end'] >= click_index:
    #                 self.test_collection.update({"_id": ObjectId(self.obj_id)}, {'$set': {x+'.inChain': False}})
    def del_oneoccur(self,click_index1,click_index2):
        # print(self.int_id_cursor)
        # print(click_index)
        dic_case = self.getOneCase(self.getcurrent_objid())
        for x in dic_case:
            if 'occur' in x:
                if dic_case[x]['str_begin'] <= click_index1 and dic_case[x]['str_end'] >= click_index2:
                    self.test_collection.update({"_id": ObjectId(self.obj_id)}, {'$set': {x+'.inChain': False}})


    def get_hazard_sub_list(self):
        #print('helo')
        lst_hazard_sub = []
        i=1
        dic_case = self.getOneCase(self.getcurrent_objid())

        for x in dic_case:
            if 'hazard_sub' in x:
               lst_hazard_sub.append(x)

        return lst_hazard_sub

    def get_atrisk_list(self):
        #print('helo')
        lst_atrisk = []
        i=1
        dic_case = self.getOneCase(self.getcurrent_objid())

        for x in dic_case:
            if 'atrisk' in x:
               lst_atrisk.append(x)

        return lst_atrisk


    def get_occur_list(self):
        '''案例中记录了多少不同的动词'''
        #print('helo')
        lst_occur = []
        i=1
        has_occur = self.test_collection.find({'fact' + str(i) : {'$exists': 1}, "_id": ObjectId(self.obj_id)}).count()
        while has_occur == 1:
            lst_occur.append('fact' + str(i))
            i = i+1
            has_occur =  self.test_collection.find({'fact' + str(i): {'$exists': 1},"_id": ObjectId(self.obj_id)}).count()
        #print(lst_occur)
        #print(has_occur)
        return lst_occur

    def has_equiz(self):
        '''TODO 统计？'''
        lst_equiz = []
        i=1
        int_equiz = self.test_collection.find({'Eqinv' + str(i) + '.type': {'$exists': 1}, "_id": ObjectId(self.obj_id)}).count()
        while int_equiz == 1:
            lst_equiz.append('Eqinv' + str(i))
            i = i+1
            int_equiz =  self.test_collection.find({'Eqinv' + str(i) + '.type': {'$exists': 1},"_id": ObjectId(self.obj_id)}).count()
        #print(lst_equiz)
        return lst_equiz

    def _find_occur(self):
        '''遍历每一个动词，记录每一个动词在案例中出现的情况,建立词典集合'''
        dic_occur = {}#{'text':'',"str_begin":0,'str_end':0}
        for j,r in enumerate(self._rawtext):   #遍历每一个间接原因的list
            # 以句子为依据进行找词
            sentence = self.para_to_sen(r)
            wordcursor = 0  # 字符串的开始索引
            for s in sentence:
                # print(s)
                for y in self.db_verb_types.find({}):#, {"_id": 0, "elements": 1}):   #遍历每一个fact的list
                    dic_occurs = []
                    y_judge=[]
                    # for i in range(len(y["elements"])):  #遍历每一个词向量
                    #     if (y["elements"][i]in s):
                    #         y_judge.append(y["elements"][i])
                    for i in y["elements"]:  #遍历每一个词向量
                        if (i in s):
                            y_judge.append(i)
                        else:
                            break
                    if y_judge == y["elements"]:
                        # for i in range(len(y_judge)):
                        for i in y_judge:
                            int_keystart = str(r).find( i , wordcursor , len(r))  #查找字符串对应的开始索引值
                            if  int_keystart != -1:  #说明该案例包含所查询的动词
                                dic_occur["text"]= i    #字典text键的值为动词
                                dic_occur["str_begin"] = int_keystart  # + linenum   #字典的str_begin键的值为动词开始索引值
                                dic_occur["str_end"] = int_keystart + len(i)  # + linenum #字典的str_end键的值为动词买的结束索引值
                                dic_occurs.append(dic_occur.copy())

                        dic_occ_dirs = []
                        dic1 = []
                        dic2 = []
                        dic3 = []
                        dic4 = y['type']
                        dic5 = y['stakeholder']
                        #dic6 = y['role_dis']
                        dic7 = y['role_dis_type']
                        dic8 = j
                        # for i in range(len(dic_occurs)):
                        for i in dic_occurs:
                            dic1.append(i['text'])
                            dic2.append(i['str_begin'])
                            dic3.append(i['str_end'])
                            #dic4.append(dic_occurs[i]['class'])
                        dic_occ_dirs.append(dic1)  # text
                        dic_occ_dirs.append(dic2)  # str_begin
                        dic_occ_dirs.append(dic3)  # str_end
                        dic_occ_dirs.append(dic4)  # type
                        dic_occ_dirs.append(dic5)  # 主体
                        #dic_occ_dirs.append(dic6)  # 角色错位x
                        dic_occ_dirs.append(dic7)  # 角色错位分类
                        dic_occ_dirs.append(dic8)  # 间接段落
                        self._db_con_occur(dic_occ_dirs)
                wordcursor += len(s)+1
        return dic_occur

    # def _find_occur(self):
    #     '''遍历每一个动词，记录每一个动词在案例中出现的情况,建立词典集合'''
    #     dic_occur = {}#{'text':'',"str_begin":0,'str_end':0}
    #     #print('dic_occur: %s' %dic_occur)
    #    # i = 0
    #     wordcursor = 0  #字符串的开始索引
    #     #while (i < len(self._rawtext)):
    #     linenum = 0
    #     for j in range(len(self._rawtext)):   #遍历每一个间接原因的list
    #         #print(self._rawtext[j])
    #         for y in self.db_verb_types.find({}, {"_id": 0, "elements": 1}):   #遍历每一个fact的list
    #             dic_occurs = []
    #             y_judge=[]
    #             for i in range(len(y["elements"])):
    #                 if (y["elements"][i]in self._rawtext[j]):
    #                         #print(lst_raw_word[i])
    #                         #print("%s存在"%y["elements"])
    #                     y_judge.append(y["elements"][i])
    #             if y_judge==y["elements"]:
    #                 for i in range(len(y_judge)):
    #                     int_keystart = str(self._rawtext[j]).find(y_judge[i],wordcursor,len(self._rawtext[j]))  #查找字符串对应的开始索引值
    #                     if  int_keystart != -1:  #说明该案例包含所查询的动词
    #                         dic_occur["text"]= y_judge[i]    #字典text键的值为动词
    #                         dic_occur["str_begin"] = int_keystart# + linenum   #字典的str_begin键的值为动词开始索引值
    #                         dic_occur["str_end"] = int_keystart + len(y_judge[i])# + linenum #字典的str_end键的值为动词买的结束索引值
    #                         #wordcursor = dic_occur["str_end"]
    #                         #print("here %s"%dic_occur)
    #                         #self._refresh_occur(dic_occur)
    #                         #break
    #                         dic_occurs.append(dic_occur.copy())
    #                         #continue
    #                 #self._refresh_occur(dic_occurs)
    #                 #print("%s：字典建立成功" % dic_occurs)
    #                 #i = i + 1
    #                 dic_occ_dirs = []
    #                 dic1 = []
    #                 dic2 = []
    #                 dic3 = []
    #                 dic4 =j
    #                 for i in range(len(dic_occurs)):
    #                     dic1.append(dic_occurs[i]['text'])
    #                     dic2.append(dic_occurs[i]['str_begin'])
    #                     dic3.append(dic_occurs[i]['str_end'])
    #                 dic_occ_dirs.append(dic1)
    #                 dic_occ_dirs.append(dic2)
    #                 dic_occ_dirs.append(dic3)
    #                 dic_occ_dirs.append(dic4)
    #                 #print(dic_occ_dirs)
    #                 self._refresh_occur(dic_occ_dirs)
    #         #linenum += len(self._rawtext[j])+1
    #     return dic_occur

    def para_to_sen(self,paragraph):
        ''' 段落切分成句子'''
        pattern = '[,.;?!，。；？！]'
        sentence = re.split(pattern, paragraph)
        # print(sentence)
        return sentence

    def _has_occur_(self,dic_occ_dirs):
        '''判断是否fact已经记录在案例库中'''
        dic_case = self.getOneCase(self.getcurrent_objid())
        has_exist = False
        for x in dic_case:
            if 'fact' in x:
                #判断是不是已经存在
                #if not dic_case[x]["inChain"]:
                if dic_case[x]['str_begin'] == dic_occ_dirs[1] and dic_case[x]['str_end'] == dic_occ_dirs[2] \
                        and dic_case[x]['str_in'] == dic_occ_dirs[6]:
                        has_exist = True
                        break
        return has_exist


    def _db_con_hazard_sub(self,dic_hazard_sub):
            hazard_sub_id = 'hazard_sub'+str(len(self.get_hazard_sub_list())+1)

            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {hazard_sub_id+'.text': dic_hazard_sub['text']}})
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {hazard_sub_id+'.ID': hazard_sub_id}})
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {hazard_sub_id+'.str_begin': dic_hazard_sub['str_begin']}})
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {hazard_sub_id+'.str_end': dic_hazard_sub['str_end']}})
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {hazard_sub_id+'.target': dic_hazard_sub['target']}})
            #=======type是为了给以后留个口子，可以归类事故用的
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {hazard_sub_id+'.type': 'hazard_sub'}})
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {hazard_sub_id+'.inChain': True}})

    def _db_con_atrisk(self, dic_atrisk):
            atrisk_id = 'atrisk'+str(len(self.get_atrisk_list())+1)

            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {atrisk_id+'.text': dic_atrisk['text']}})
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {atrisk_id+'.ID': atrisk_id}})
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {atrisk_id+'.str_begin': dic_atrisk['str_begin']}})
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {atrisk_id+'.str_end': dic_atrisk['str_end']}})
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {atrisk_id+'.target': dic_atrisk['target']}})
            #=======type是为了给以后留个口子，可以归类事故用的
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {atrisk_id+'.type': 'atrisk'}})
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {atrisk_id+'.inChain': True}})


    def _db_con_occur(self, dic_occ_dirs):
        ''' 在案例中，建立一个新的动词出现情况'''
        if not self._has_occur_(dic_occ_dirs):
        #     occur_id = 'occur'+str(len(self.get_occur_list())+1)
        #
        #     self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {occur_id+'.text': dic_occur['text']}})
        #     self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {occur_id+'.ID': occur_id}})
        #     self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {occur_id+'.str_begin': dic_occur['str_begin']}})
        #     self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {occur_id+'.str_end': dic_occur['str_end']}})
        #     #=======type是为了给以后留个口子，可以归类事故用的
        #     self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {occur_id+'.type': 'occur'}})
        #     self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {occur_id+'.inChain': True}})
            occur_id = 'fact' + str(len(self.get_occur_list()) + 1)
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {occur_id + '.text': dic_occ_dirs[0]}})
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {occur_id + '.ID': occur_id}})
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)},{'$set': {occur_id + '.str_begin': dic_occ_dirs[1]}})
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)},{'$set': {occur_id + '.str_end': dic_occ_dirs[2]}})
            # =======type是为了给以后留个口子，可以归类事故用的
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {occur_id + '.type': dic_occ_dirs[3]}})
            #self.test_collection.update_one({"_id": ObjectId(self.obj_id)},{'$set': {occur_id + '.stakeholder': dic_occ_dirs[4]}})
            #self.test_collection.update_one({"_id": ObjectId(self.obj_id)},{'$set': {occur_id + '.role_dis_type': dic_occ_dirs[5]}})
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)},{'$set': {occur_id + '.str_in': dic_occ_dirs[6]}})
            #self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {occur_id + '.inChain': True}})


    def _refresh_occur(self, dic_occur):
        '''TODO 在案例库中建立动词出现情况'''
        #print('='*20)
        dic_case = self.getOneCase(self.getcurrent_objid())
        #print("dic_case:%s" %dic_case)
        total_newword = True
        #for x in dic_case:  #记录中每一个字段和键
            #print("x:%s" % x)
        #     if 'occur' in x:
        #         #如果是停词，逻辑删除
        #         #if dic_case[x]['text'] in self.stopwords:
        #             #self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {x + '.inChain': False}})   #不在放在链中
        #             #print('stopword  '+dic_occur['text'])
        #         #如果原来就存在保持原样
        #         if dic_case[x]['str_begin'] == dic_occur['str_begin'] and dic_case[x]['str_end'] == dic_occur['str_end']:
        #             total_newword = False
        #             #self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {x + '.inChain': True}})
        #             #total_newword = True
        #             pass
        #         #如果新的包含老的
        #         if (dic_case[x]['str_begin'] > dic_occur['str_begin'] and dic_case[x]['str_end'] <= dic_occur['str_end']) \
        #                  or (dic_case[x]['str_begin'] >= dic_occur['str_begin'] and dic_case[x]['str_end'] < dic_occur['str_end']):
        #         # if (dic_case[x]['str_begin'] >= dic_occur['str_begin'] and dic_case[x]['str_end'] <= dic_occur['str_end']):
        #         #     total_newword = False
        #             if dic_case[x]["inChain"] == True:
        #                 #那么删了老的
        #                 self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {x + '.inChain': False}})
        #                 #然后添加一个新的
        #                 #print('inchain')
        #                 self._db_con_occur(dic_occur)
        #             else:
        #                 self._db_con_occur(dic_occur)
        if total_newword:
            self._db_con_occur(dic_occur)

    def upload_occur_2tag(self):
        ''' 将链中的动词添加到动词库中'''
        dic_tag = self._get_occur_tags()   #获取当前动词库中的词和词性
        dic_case = self.getOneCase(self.getcurrent_objid())    #获取当前案例记录
        #print(dic_case['transversion'])
        for x in dic_case:
            if 'occur' in x:
                if dic_case[x]['text'] not in dic_tag.keys():   #案例中出现的动词不在动词库里面，若该词在链中，则应该把该词加到动词库中
                    if dic_case[x]['inChain'] == True:
                        self.db_verb_types.insert({"elements": dic_case[x]['text'],"account": 3, "nouns": "x"})
                        print('ok')
                        dic_tag = self._get_occur_tags()


    def _get_occur_tags(self):
        '''获取当前动词库中的词性 '''
        #lst_tag=[]
        dic_tag={}
        for x in self.db_verb_types.find({}, {"_id": 0, "elements": 1, "nouns": 1}):
            dic_tag[x['elements']] = x['nouns']
        #print('dic_tag%s:' %dic_tag)
            #lst_tag.append(x['elements'])
        return dic_tag

    def create_new_atrisk(self, dic_atrisk, occur_click_index):
        atrisk_exist = False
        dic_case = self.getOneCase(self.getcurrent_objid())
        for x in dic_case:
            if 'occur' in x:
                if dic_case[x]['str_begin'] <= occur_click_index and dic_case[x]['str_end'] >= occur_click_index:
                    dic_atrisk['target'] = dic_case[x]['str_begin']

        for x in dic_case:
            if 'hazard_sub' in x:
                if dic_case[x]['str_begin'] == dic_atrisk['str_begin'] and dic_case[x]['str_end'] == dic_atrisk['str_end']:
                        self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {x + '.inChain': True}})
                        tkinter.messagebox.showinfo('Info', 'New occur has been contructed')
                        hazard_sub_exist = True
                        break
                #else: #如果没有标记过的
        if not atrisk_exist:
            self._db_con_atrisk(dic_atrisk)

    def create_new_hazard_sub(self, dic_hazard_sub,occur_click_index):
        hazard_sub_exist = False
        dic_case = self.getOneCase(self.getcurrent_objid())
        for x in dic_case:
            if 'occur' in x:
                if dic_case[x]['str_begin'] <= occur_click_index and dic_case[x]['str_end'] >= occur_click_index:
                    dic_hazard_sub['target'] = dic_case[x]['str_begin']

        for x in dic_case:
            if 'hazard_sub' in x:
                if dic_case[x]['str_begin'] == dic_hazard_sub['str_begin'] and dic_case[x]['str_end'] == dic_hazard_sub['str_end']:
                        self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {x + '.inChain': True}})
                        tkinter.messagebox.showinfo('Info', 'New occur has been contructed')
                        hazard_sub_exist = True
                        break
                #else: #如果没有标记过的
        if not hazard_sub_exist:
            self._db_con_hazard_sub(dic_hazard_sub)


    def create_new_occur(self, dic_occur):
        '''创建新的occur'''
        occur_exist = False
        dic_case = self.getOneCase(self.getcurrent_objid())
        for x in dic_case:
            if 'occur' in x:
                #判断是不是已经存在
                #if not dic_case[x]["inChain"]:
                if dic_case[x]['str_begin'] == dic_occur['str_begin'] and dic_case[x]['str_end'] == dic_occur['str_end']:
                    if dic_case[x]["inChain"]==False: #如果以前被删掉过，可以重新添加到链中
                        self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {x + '.inChain': True}})
                        tkinter.messagebox.showinfo('Info', 'New occur has been contructed')
                        occur_exist = True
                        break
                    else: #如果已经是标记过的
                        tkinter.messagebox.showinfo('Info', 'This occur has been existed')
                        occur_exist = True
                        break
                if (dic_occur['str_begin']<= dic_case[x]['str_end'] and dic_occur['str_begin'] >= dic_case[x]['str_begin']) \
                        or (dic_occur['str_end']>= dic_case[x]['str_begin']  and dic_occur['str_end'] <= dic_case[x]['str_end']):
                    #部分重复
                    if dic_case[x]["inChain"] == True:  # 本来就是有标记的
                        self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {x + '.inChain': False}})
                        self._db_con_occur(dic_occur)
                        tkinter.messagebox.showinfo('Info', 'New occur has been contructed 子集')
                        occur_exist = True
                        # print('标记开始',dic_case[x]['str_begin'])
                        # print('实际开始',dic_occur['str_begin'])
                        # print('标记',dic_case[x]['str_end'])
                        # print('实际',dic_occur['str_end'])
                        break
                else:
                    pass
        if occur_exist == False:
            self._db_con_occur(dic_occur)
            tkinter.messagebox.showinfo('Info', 'New occur has been contructed 空集')


    def _db_con_Eqinv(self,dic_Eqinv):
        Eqinv_id = 'Eqinv'+str(len(self.has_equiz())+1)
        self.test_collection.update({"_id": ObjectId(self.obj_id)}, {'$set': {Eqinv_id+'.text': dic_Eqinv['text']}})
        self.test_collection.update({"_id": ObjectId(self.obj_id)}, {'$set': {Eqinv_id+'.ID': Eqinv_id}})
        self.test_collection.update({"_id": ObjectId(self.obj_id)}, {'$set': {Eqinv_id+'.str_begin': dic_Eqinv['str_begin']}})
        self.test_collection.update({"_id": ObjectId(self.obj_id)}, {'$set': {Eqinv_id+'.str_end': dic_Eqinv['str_end']}})
        self.test_collection.update({"_id": ObjectId(self.obj_id)}, {'$set': {Eqinv_id+'.type': dic_Eqinv['type']}})
        self.test_collection.update({"_id": ObjectId(self.obj_id)}, {'$set': {Eqinv_id+'.in': dic_Eqinv['in']}})
        self.test_collection.update({"_id": ObjectId(self.obj_id)}, {'$set': {Eqinv_id+'.out': dic_Eqinv['out']}})

    def getOneCase(self, objid):
        '''获取当前id的对应记录'''
        dic = self.test_collection.find_one({"_id": ObjectId(objid)})
        self._rawtext = dic['间接原因']    #将记录中transversion字段内容存放到_rawtext中
        #print(self._rawtext)
        return dic


    def get_rawtext(self,dbcursor):
        dic = self.getOneCase(dbcursor)
        return dic['transversion']

    def initial_db(self):
        #jieba.load_userdict(self.userdict)
        self.stopwords = self._stopwordslist(self.str_dir)  # 加载停留词
        words = pseg.cut(self._rawtext)
        list_include_tag = ['an', 'ad', 'b', 'f', 'j', 'l', 'm', 'n', 'nt', 'nx', 'nz', 's', 'v', 'vg', 'vn', 'q']
        list_word = [] #处理过分词数列
        list_raw_word = [] #分词数列
        list_tag = [] #处理过的词性标注数列
        list_raw_tag = [] #词性标注数列
        list_ver_pos = [] #已标注动词位置数列
        list_noun_pos = [] #名词位置数列

        for word, flag in words:
            list_raw_word.append(word)
            list_raw_tag.append(flag)
            if (word not in self.stopwords) and (flag in list_include_tag):
                list_tag.append(flag)
                list_word.append(word)
        #self._find_occur(list_raw_word)
        dic_occur = {'text':'',"str_begin":0,'str_end':0}
        i = 0
        wordcursor = 0
        while (i < len(list_raw_word)):
            for y in self.db_verb_types.find({}, {"_id": 0, "elements": 1}):
                # 没有区分动词还是名词，只要包含标注的动词就输出
                if (y["elements"] in list_raw_word[i]):
                    int_keystart = str(self._rawtext).find(list_raw_word[i],wordcursor,len(self._rawtext))
                    if  int_keystart != -1:
                        dic_occur["text"]= list_raw_word[i]
                        dic_occur["str_begin"] = int_keystart
                        dic_occur["str_end"] = int_keystart + len(list_raw_word[i])
                        wordcursor = dic_occur["str_end"]
                        self._db_con_occur(dic_occur)
                        break
            i = i + 1

    def add_2stopword(self,click_index):
        dic_case = self.getOneCase(self.getcurrent_objid())

        for x in dic_case:
            if 'occur' in x:
                if dic_case[x]['str_begin'] <= click_index and dic_case[x]['str_end'] >= click_index:
                    new_stop = dic_case[x]['text']
                    break
        f1 = open(self.str_dir, 'r+',encoding='utf-8')
        f1.read()
        f1.write('\n'+new_stop)
        f1.close()
        self.del_oneoccur(click_index)

    def get_occur_type(self, occur_name):
        _type = 'x'

        for x in self.db_verb_types.find({}, {"_id": 0, "elements": 1, "nouns": 1}):
            if x['elements'] == occur_name:
                _type = x['nouns']

        return _type




if __name__ == '__main__':
#=====test class=====
# # b=db_occur_equiz('5ce509f4f5891728b083177d',cleardb=True)
# # b.nlp()
# b=db_occur_equiz('5ce509f4f5891728b083176d',cleardb=True)
# b.nlp()
# # b=db_occur_equiz('5ce509f4f5891728b083176d',cleardb=True)
# # b.nlp()
# # dic_occ = {'text':''}
# # dic_occ['text'] = 'kkd'
# # b.con_occur(dic_occ)
# # b.con_occur(dic_occ)

    i = 1
    while i < 145:


        print(i)
        b = db_occur_equiz(i, cleardb=True)
        # b.getOneCase(b.getcurrent_objid())
        # b.nlp()
        i = i+1
    # b = db_occur_equiz(17, cleardb=True)
    # b.getOneCase(b.getcurrent_objid())
    # b.initial_db()

    # b = db_occur_equiz(29)
    # b.upload_occur_2tag()




