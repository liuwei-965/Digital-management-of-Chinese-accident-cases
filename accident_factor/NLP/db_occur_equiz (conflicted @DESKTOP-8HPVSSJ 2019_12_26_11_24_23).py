from pymongo import MongoClient
from bson.objectid import ObjectId
import jieba
import jieba.posseg as pseg
import tkinter.messagebox


class db_occur_equiz():
    myclient = MongoClient('mongodb://localhost:27017/')

    mydb = myclient["tank_accidents"]

    test_collection = mydb["油罐_details_bak"]
    db_verb_types = mydb["verb_types"]

    obj_id=''
    _rawtext= ''


    def __init__(self,id_cursor, cleardb = False):
        if __name__ == '__main__':
            self.str_dir = '../temp/stopwords.txt'
            self.userdict = '../temp/userdict.txt'
        else:
            self.str_dir = './temp/stopwords.txt'
            self.userdict = './temp/userdict.txt'
        self.lst_objid = self._get_idlist()
        if -1<id_cursor< len(self.lst_objid):
            self.int_id_cursor = id_cursor
        else:
            self.int_id_cursor = 0

        self.obj_id= self.lst_objid[self.int_id_cursor]
        if cleardb:
            self._cleardb()

    def getcurrent_objid(self):
        return  self.obj_id

    def get_case_collection(self):
        lst = self._get_idlist()
        return self.test_collection.find_one({"_id": ObjectId(lst[self.int_id_cursor])})


    def _get_idlist(self):
        lst_id = []
        i = 1
        for x in self.test_collection.find({},{"_id":1}):
            lst_id.append(x['_id'])
            # print(x['_id'])
            # print(i)
            # i=i+1
        return lst_id

    #每次进入一个case 重新学习occur
    def add_terminology_dic(self):
        f = open(self.userdict, "a+", encoding='utf-8')
        f.write('流淌火  \n')
        f.close()


    def nlp(self):
        jieba.load_userdict(self.userdict)
        self.stopwords = self._stopwordslist(self.str_dir)  # 加载停留词
        words = pseg.cut(self._rawtext)
        list_raw_word = [] #分词数列
        list_raw_tag = [] #词性标注数列

        for word, flag in words:
            list_raw_word.append(word)
            list_raw_tag.append(flag)
        self._find_occur(list_raw_word)


    def _stopwordslist(self,filepath):
        stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
        return stopwords



    def _cleardb(self):
        #print('clear db')
        for x in self.get_occur_list():
            self.test_collection.update({"_id": ObjectId(self.obj_id)}, {'$unset': {x: 1}})
        for x in self.has_equiz():
            self.test_collection.update({"_id": ObjectId(self.obj_id)}, {'$unset': {x: 1}})


    def add_newoccur_to_verbtypes(self):
        print('done')

    def del_oneoccur(self,click_index):
        # print(self.int_id_cursor)
        # print(click_index)
        dic_case = self.getOneCase(self.getcurrent_objid())

        for x in dic_case:
            if 'occur' in x:
                if dic_case[x]['str_begin'] <= click_index and dic_case[x]['str_end'] >= click_index:
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
        #print('helo')
        lst_occur = []
        i=1
        has_occur = self.test_collection.find({'occur' + str(i) : {'$exists': 1}, "_id": ObjectId(self.obj_id)}).count()
        while has_occur == 1:
            lst_occur.append('occur' + str(i))
            i = i+1
            has_occur =  self.test_collection.find({'occur' + str(i): {'$exists': 1},"_id": ObjectId(self.obj_id)}).count()
        #print(lst_occur)
        return lst_occur

    def has_equiz(self):
        lst_equiz = []
        i=1
        int_equiz = self.test_collection.find({'Eqinv' + str(i) + '.type': {'$exists': 1}, "_id": ObjectId(self.obj_id)}).count()
        while int_equiz == 1:
            lst_equiz.append('Eqinv' + str(i))
            i = i+1
            int_equiz =  self.test_collection.find({'Eqinv' + str(i) + '.type': {'$exists': 1},"_id": ObjectId(self.obj_id)}).count()
        #print(lst_equiz)
        return lst_equiz

    def _find_occur(self,lst_raw_word:list):
        dic_occur = {'text':'',"str_begin":0,'str_end':0}
        i = 0
        wordcursor = 0
        while (i < len(lst_raw_word)):
            for y in self.db_verb_types.find({}, {"_id": 0, "elements": 1}):
                # 没有区分动词还是名词，只要包含标注的动词就输出
                if (y["elements"] in lst_raw_word[i]):
                    #print(lst_raw_word[i])
                    int_keystart = str(self._rawtext).find(lst_raw_word[i],wordcursor,len(self._rawtext))
                    if  int_keystart != -1:
                        dic_occur["text"]= lst_raw_word[i]
                        dic_occur["str_begin"] = int_keystart
                        dic_occur["str_end"] = int_keystart + len(lst_raw_word[i])
                        wordcursor = dic_occur["str_end"]
                        self._refresh_occur(dic_occur)
                        break
            i = i + 1
        return dic_occur

    def _has_occur_(self,dic_occur):
        dic_case = self.getOneCase(self.getcurrent_objid())
        has_exist = False

        for x in dic_case:
            if 'occur' in x:
                #判断是不是已经存在
                #if not dic_case[x]["inChain"]:
                if dic_case[x]['str_begin'] == dic_occur['str_begin'] and dic_case[x]['str_end'] == dic_occur['str_end']:
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


    def _db_con_occur(self, dic_occur):
        if not self._has_occur_(dic_occur):
            occur_id = 'occur'+str(len(self.get_occur_list())+1)
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {occur_id+'.text': dic_occur['text']}})
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {occur_id+'.ID': occur_id}})
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {occur_id+'.str_begin': dic_occur['str_begin']}})
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {occur_id+'.str_end': dic_occur['str_end']}})
            #=======type是为了给以后留个口子，可以归类事故用的
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {occur_id+'.type': 'occur'}})
            self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {occur_id+'.inChain': True}})
    def _refresh_occur(self, dic_occur):
        #print('='*20)
        dic_case = self.getOneCase(self.getcurrent_objid())
        total_newword = True
        for x in dic_case:
            if 'occur' in x:
                #如果是停词，逻辑删除
                if dic_case[x]['text'] in self.stopwords:
                    self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {x + '.inChain': False}})
                    #print('stopword  '+dic_occur['text'])
                #如果原来就存在保持原样
                if dic_case[x]['str_begin'] == dic_occur['str_begin'] and dic_case[x]['str_end'] == dic_occur['str_end']:
                    total_newword = False
                    pass
                #如果新的包含老的
                if (dic_case[x]['str_begin'] > dic_occur['str_begin'] and dic_case[x]['str_end'] <= dic_occur['str_end']) or (dic_case[x]['str_begin'] >= dic_occur['str_begin'] and dic_case[x]['str_end'] < dic_occur['str_end']):
                    total_newword = False
                    if dic_case[x]["inChain"] == True:
                        #那么删了老的
                        self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {x + '.inChain': False}})
                        #然后见一个新的
                        #print('inchain')
                        self._db_con_occur(dic_occur)
                    else:
                        self._db_con_occur(dic_occur)
        if total_newword:
            self._db_con_occur(dic_occur)

    def upload_occur_2tag(self):
        dic_tag = self._get_occur_tags()
        dic_case = self.getOneCase(self.getcurrent_objid())
        #print(dic_case['transversion'])
        for x in dic_case:
            if 'occur' in x:
                if dic_case[x]['text'] not in dic_tag.keys():
                    if dic_case[x]['inChain'] == True:
                        self.db_verb_types.insert({"elements": dic_case[x]['text'],"account": 3, "nouns": "x"})
                        print('ok')
                        dic_tag = self._get_occur_tags()



    def _get_occur_tags(self):
        #lst_tag=[]
        dic_tag={}
        for x in self.db_verb_types.find({}, {"_id": 0, "elements": 1, "nouns": 1}):
            dic_tag[x['elements']] = x['nouns']
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
        occur_exist = False
        dic_case = self.getOneCase(self.getcurrent_objid())
        for x in dic_case:
            if 'occur' in x:
                #判断是不是已经存在
                #if not dic_case[x]["inChain"]:
                if dic_case[x]['str_begin'] == dic_occur['str_begin'] and dic_case[x]['str_end'] == dic_occur['str_end']:
                    if dic_case[x]["inChain"]==False: #如果以前被删掉过
                        self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {x + '.inChain': True}})
                        tkinter.messagebox.showinfo('Info', 'New occur has been contructed')
                        occur_exist = True
                        break
                    else: #如果已经是标记过的
                        tkinter.messagebox.showinfo('Info', 'This occur has been existed')
                        occur_exist = True
                        break
                if (dic_occur['str_begin']<= dic_case[x]['str_end'] and dic_occur['str_begin'] >= dic_case[x]['str_begin']) or (dic_occur['str_end']>= dic_case[x]['str_begin']  and dic_occur['str_end'] <= dic_case[x]['str_end']):
                    if dic_case[x]["inChain"] == True:  # 本来就是有标记的
                        self.test_collection.update_one({"_id": ObjectId(self.obj_id)}, {'$set': {x + '.inChain': False}})
                        self._db_con_occur(dic_occur)
                        tkinter.messagebox.showinfo('Info', 'New occur has been contructed 子集')
                        occur_exist = True
                        # print('标记开始',dic_case[x]['str_begin'])
                        # print('实际开始',dic_occur['str_begin'])
                        #
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
        dic = self.test_collection.find_one({"_id": ObjectId(objid)})
        self._rawtext = dic['transversion']
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
        dic_verb_types = {}
        #print(occur_name)

        for x in self.db_verb_types.find({}, {"_id": 0, "elements": 1, "nouns": 1}):
            dic_verb_types[x["elements"]]=x["nouns"]
        return dic_verb_types.get(occur_name,'x')







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




