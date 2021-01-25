import sys
sys.path.append('.\GUI')
sys.path.append('..\\NLP')
sys.path.append('..\\temp')

import os
from bson.objectid import ObjectId
os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz2.38/bin/'
#os.environ["PATH"] += os.pathsep + 'E:/Program Files (x86)/Graphviz2.38/bin/'

from NLP.db_occur_equiz import db_occur_equiz
from graphviz import Digraph

worker = ['不安全作业','无证上岗','工人隐性知识不足（能力、经验、知识、安全意识）']
worker_num = ['1-1','1-2','1-3']
contractor = ['主体责任落实不到位','未制定施工方案','安全、质量监管与控制','规则、制度不健全','安全文化、认知不足','防护措施、设备及警示不到位','不合理施工','教育培训不到位','现场条件','组织、指挥不当','资质审查','事故处理不当','不具备相应资质']
contractor_num = ['2-1','2-2','2-3','2-4','2-5','2-6','2-7','2-8','2-9','2-10','2-11','2-12','2-13']
client = ['供方管理','违法动工','监管承包商','验收工程','档案管理']
client_num = ['3-1','3-2','3-3','3-4','3-5']
supervision = ['监督、控制承包商','未向业主汇报情况','不具备监理资格','监理隐性知识不足（能力、经验、知识、安全意识）']
supervision_num = ['4-1','4-2','4-3','4-4']
government = ['监督、指导不到位','处置不严','组织、机制、制度不健全']
government_num = ['5-1','5-2','5-3']
supplier = ['材料设备质量不合格']
supplier_num = ['6']
other = ['设计勘察']
other_num = ['7']
occur_num = 0

class LR_RenderFlow():

    def __init__(self, dbcursor,db,nview=False):
        self.db = db_occur_equiz(dbcursor)
        self.objid = self.db.getcurrent_objid()
        self.dic_role_node = {'shape': 'box', 'style': 'radial', 'fillcolor': 'white:red'}  # 链中形状设置
        self.dic_normal_node ={'shape':'egg','style':'radial','fillcolor':'white:lightblue'}   #链中形状设置
        self.dic_normal_node1 = {'shape': 'egg', 'style': 'radial', 'fillcolor': 'white:blue'}  # 链中形状设置
        self.dic_normal_node2 = {'shape': 'egg', 'style': 'radial', 'fillcolor': 'white:yellow'}  # 链中形状设置
        self.dic_normal_node3 = {'shape': 'egg', 'style': 'radial', 'fillcolor': 'white:green'}  # 链中形状设置
        self.dic_normal_node4 = {'shape': 'egg', 'style': 'radial', 'fillcolor': 'white:pink'}  # 链中形状设置
        self.dic_normal_node5 = {'shape': 'egg', 'style': 'radial', 'fillcolor': 'white:brown'}  # 链中形状设置
        self.dic_normal_node6 = {'shape': 'egg', 'style': 'radial', 'fillcolor': 'white:white'}  # 链中形状设置
        self.dic_focus_one_node ={'shape':'egg','style':'radial','fillcolor':'white:red'}
        self.dic_hazard_sub_node ={'shape':'box','style':'radial','fillcolor':'darkorange:grey'}
        self.dic_atrisk_node ={'shape':'box','style':'radial','fillcolor':'cyan:grey'}
        self.nview = nview
        #occur_num += len(self.db.get_occur_list())
        #self.objid = dbcursor
        if __name__ == '__main__':
            self.png_dir = '../temp/'
        else:
            self.png_dir = './temp/'
        self.g = Digraph('test_occur_graphviz', directory=self.png_dir, format='png')
        self.renderWhole()

    def typenum_to_type(self,typenum):
        if typenum in worker_num:
            index = worker_num.index(typenum)
            return worker[index]
        elif typenum in contractor_num:
            index = contractor_num.index(typenum)
            return contractor[index]
        elif typenum in client_num:
            index = client_num.index(typenum)
            return client[index]
        elif typenum in supervision_num:
            index = supervision_num.index(typenum)
            return supervision[index]
        elif typenum in government_num:
            index = government_num.index(typenum)
            return government[index]
        elif typenum in supplier_num:
            index = supplier_num.index(typenum)
            return supplier[index]
        elif typenum in other_num:
            index = other_num.index(typenum)
            return other[index]
        else:
            return "未分类"

    # def renderWhole(self):
    #     self.delete_exit_occur_png('occur.png')  #删除当前图片
    #     dic_case = self.db.getOneCase(self.objid)
    #     lst_node = []
    #     dic_unorder_nodes = {}
    #     dic_hazrd_sub = {}
    #     dic_atrisk = {}
    #     self.g.clear()
    #
    #     for x in dic_case:
    #         if 'occur' in x:
    #             if dic_case[x]["inChain"]:
    #                 with self.g.subgraph(name='cluster_0') as g_occur:
    #                     g_occur.attr(color='lightgrey')
    #                     g_occur.attr('node', self.dic_normal_node)
    #                     g_occur.node(dic_case[x]['ID'], label=dic_case[x]['text'],fontname="SimHei")
    #                     dic_unorder_nodes[dic_case[x]['ID']] = dic_case[x]['str_begin']
    #         if 'hazard_sub' in x:
    #             if dic_case[x]["inChain"]:
    #                 with self.g.subgraph(name='cluster_1') as g_hazard:
    #                     g_hazard.attr(color='white',rank = 'max')
    #                     g_hazard.attr('node', self.dic_hazard_sub_node)
    #                     g_hazard.node(dic_case[x]['ID'], label=dic_case[x]['text'],fontname="SimHei")
    #                     dic_hazrd_sub[dic_case[x]['ID']] = dic_case[x]['target']
    #         if 'atrisk' in x:
    #             if dic_case[x]["inChain"]:
    #                 with self.g.subgraph(name='cluster_2') as g_atrisk:
    #                     g_atrisk.attr(color='white',rank = 'max')
    #                     g_atrisk.attr('node', self.dic_atrisk_node)
    #                     g_atrisk.node(dic_case[x]['ID'], label=dic_case[x]['text'],fontname="SimHei")
    #                     dic_atrisk[dic_case[x]['ID']] = dic_case[x]['target']
    #         i = 0
    #     #按照occur出现的顺序进行排序
    #     a = sorted(dic_unorder_nodes.items(), key=lambda x: x[1], reverse=False)
    #     for y in a:
    #         lst_node.append(y[0])
    #     # self.g.edge('start', 'occur1')
    #     # self.g.edge('start', 'atrisk1')
    #     # self.g.edge('start', 'hazard_sub1')
    #     while i <= len(lst_node) - 1:
    #        if i+1 < len(lst_node) :
    #          self.g.edge(lst_node[i], lst_node[i + 1])
    #        for z in dic_hazrd_sub:
    #            if dic_hazrd_sub[z] == dic_unorder_nodes[lst_node[i]]:
    #                self.g.edge(z,lst_node[i])
    #        for q in dic_atrisk:
    #            if dic_atrisk[q] == dic_unorder_nodes[lst_node[i]]:
    #                self.g.edge(lst_node[i],q)
    #        i = i + 1
    #     self.g.render(filename='occur')
    #     #self.g.render(filename='C:\\Users\\正在输入---\\Desktop\\chain_finder\\temp\\occur')

    def renderWhole(self):  #初始批量标准化
        self.delete_exit_occur_png('occur.png')  #删除当前图片
        dic_case = self.db.getOneCase(self.objid)
        lst_node = []  #记录节点对象名称
        lst_node_lable =[]  #记录节点标签名称（类别编码）
        types = []  #记录节点标签的类别名
        dic_unorder_nodes = {}  #记录节点开始位置
        role_dis_types = []
        self.g.clear()

        for x in dic_case:    #初始批量标准化
            if 'occur' in x:
                #if dic_case[x]["inChain"]:
                    with self.g.subgraph(name='cluster_0') as g_occur:
                        g_occur.attr(color='lightgrey')  #点的样式
                        g_occur.attr('node', self.dic_normal_node)  #点的样式
                        # 生成图片节点（节点对象的名词，节点名，字体）
                        if dic_case[x]['type'] not in lst_node_lable:
                            type = self.typenum_to_type(dic_case[x]['type'])
                            #print(type)
                            lst_node_lable.append(dic_case[x]['type'])
                            if type != '未分类':
                                types.append(type)
                                #print(types)
                                g_occur.node(dic_case[x]['ID'], label= type, fontname="SimHei")  #节点标签名称
                                dic_unorder_nodes[dic_case[x]['ID']] = dic_case[x]['str_begin']  #将节点开始位置记录在字典dic_unorder_nodes中
                        #print(dic_unorder_nodes)
                    if (dic_case[x]['role_dis_type'] != '空') and (dic_case[x]['role_dis_type'] not in role_dis_types):
                        role_dis_types.append(dic_case[x]['role_dis_type'])
        if len(role_dis_types ) == 0:
            role_dis_types = ['空']
        if len(types) == 0:
            types = ['空']
        #按照occur出现的顺序进行排序
        #a = sorted(dic_unorder_nodes.items(), key=lambda x: x[0], reverse=False)
        a = dic_unorder_nodes.items()
        for y in a:
            lst_node.append(y[0])  # key,例如'occur1'
        i = 0
        while i <= len(lst_node) - 1:
           #print(i)
           if i+1 < len(lst_node) :
             self.g.edge(lst_node[i], lst_node[i + 1])
           i = i + 1
        self.g.render(filename='occur')
        #self.store_type(types,role_dis_types)  #初始批量标准化

    '''def renderWhole(self):  
        #显示角色错位的机制
        #self.delete_exit_occur_png('occur.png')  #删除当前图片
        dic_case = self.db.getOneCase(self.objid)
        global occur_num
        occur_num += len(self.db.get_occur_list())
        lst_role = []  #记录错位节点对象名称
        lst_worker = []
        lst_contractor =[]
        lst_client =[]
        lst_supervision =[]
        lst_government =[]
        lst_supplier =[]
        lst_other =[]
        #lst_node = []
        lst_node = [lst_worker,lst_contractor,lst_client ,lst_supervision,lst_government ,lst_supplier ,lst_other ]  #记录因素节点对象名称
        lst_nodes = []
        self.g.clear()

        with self.g.subgraph(name='cluster_0') as g_occur:
            g_occur.attr('node', self.dic_role_node) # 点的样式
            g_occur.edge_attr.update(arrowhead='none')  #无向边
            for type in dic_case['role_dis_types']:
                g_occur.node(type, fontname="SimHei")  # 添加点，节点标签名称
                lst_role.append(type)
            i = 0
            while i <= len(lst_role) - 1:  #添加边
                if i + 1 < len(lst_role):
                    g_occur.edge(lst_role[i], lst_role[i + 1])
                i = i + 1
        with self.g.subgraph(name='cluster_1') as g_occur:
            #g_occur.attr('node', self.dic_normal_node)  # 点的样式
            g_occur.edge_attr.update(arrowhead='none')  # 无向边
            for type in dic_case['types']:
                if type in worker:
                    with g_occur.subgraph(name='cluster_2') as p:
                        p.attr('node', self.dic_normal_node)  # 点的样式
                        p.attr(label='\t工人',fontname="SimHei")
                        p.edge_attr.update(arrowhead='none')  # 无向边
                        p.node(type, fontname="SimHei")  # 添加点，节点标签名称
                        lst_worker.append(type)

                if type in contractor:
                    with g_occur.subgraph(name='cluster_3') as p:
                        p.attr('node', self.dic_normal_node1)  # 点的样式
                        p.attr(label='\t承包商',fontname="SimHei")
                        p.edge_attr.update(arrowhead='none')  # 无向边
                        p.node(type, fontname="SimHei")  # 添加点，节点标签名称
                        lst_contractor.append(type)

                if type in client:
                    with g_occur.subgraph(name='cluster_4') as p:
                        p.attr('node', self.dic_normal_node2)  # 点的样式
                        p.attr(label='\t业主',fontname="SimHei")
                        p.edge_attr.update(arrowhead='none')  # 无向边
                        p.node(type, fontname="SimHei")  # 添加点，节点标签名称
                        lst_client.append(type)

                if type in supervision:
                    with g_occur.subgraph(name='cluster_5') as p:
                        p.attr('node', self.dic_normal_node3)  # 点的样式
                        p.attr(label='\t监理',fontname="SimHei")
                        p.edge_attr.update(arrowhead='none')  # 无向边
                        p.node(type, fontname="SimHei")  # 添加点，节点标签名称
                        lst_supervision.append(type)

                if type in government:
                    with g_occur.subgraph(name='cluster_6') as p:
                        p.attr('node', self.dic_normal_node4)  # 点的样式
                        p.attr(label='\t政府',fontname="SimHei")
                        p.edge_attr.update(arrowhead='none')  # 无向边
                        p.node(type, fontname="SimHei")  # 添加点，节点标签名称
                        lst_government.append(type)

                if type in supplier:
                    with g_occur.subgraph(name='cluster_7') as p:
                        p.attr('node', self.dic_normal_node5)  # 点的样式
                        p.attr(label='\t供应商',fontname="SimHei")
                        p.edge_attr.update(arrowhead='none')  # 无向边
                        p.node(type, fontname="SimHei")  # 添加点，节点标签名称
                        lst_supplier.append(type)

                if type in other:
                    with g_occur.subgraph(name='cluster_8') as p:
                        p.attr('node', self.dic_normal_node6)  # 点的样式
                        p.attr(label='\t其他',fontname="SimHei")
                        p.edge_attr.update(arrowhead='none')  # 无向边
                        p.node(type, fontname="SimHei")  # 添加点，节点标签名称
                        lst_other.append(type)

            for role in lst_node:
                if role != []:
                    lst_nodes.append(role)
            #print(lst_nodes)
            for i,role in enumerate(lst_nodes):
                if i < len(lst_nodes)-1:
                    g_occur.edge(lst_nodes[i][-1], lst_nodes[i+1][0])  # 添加两个子图间的边
                i = 0
                while i <= len(role) - 1:  # 添加边
                    if i + 1 < len(role):
                        g_occur.edge(role[i], role[i + 1])
                    i = i + 1

        self.g.edge_attr.update(arrowhead='normal')  # 有向边
        self.g.edge(lst_role[-1], lst_nodes[0][0], ltail='cluster_0', lhead='cluster_1')  # 添加两个子图间的边
        self.g.render(filename='occur')
        print(occur_num)'''

    def store_type(self,types,role_dis_types):
        '''在数据库中存储间接原因的类别'''
        test_collection = self.db.test_collection
        test_collection.update_one({"_id": ObjectId(self.objid)}, {'$set': {'types': types}})
        test_collection.update_one({"_id": ObjectId(self.objid)}, {'$set': {'role_dis_types': role_dis_types}})

    def focus_one_occur(self,click_index):
        self.delete_exit_occur_png('occur_focus_one.png')
        dic_case = self.db.getOneCase(self.objid)
        lst_node = []
        dic_unorder_nodes = {}
        dic_hazrd_sub = {}
        dic_atrisk = {}
        self.g.clear()

        for x in dic_case:
            if 'occur' in x:
                #如果被选中
                if dic_case[x]["inChain"]:
                    with self.g.subgraph(name='cluster_0') as g_occur:
                        g_occur.attr(color='lightgrey')
                        if dic_case[x]['str_begin'] <= click_index and dic_case[x]['str_end'] >= click_index:
                            g_occur.attr('node', self.dic_focus_one_node)
                            g_occur.node(dic_case[x]['ID'], label=dic_case[x]['text'],fontname="SimHei")
                            #lst_node.append(dic_case[x]['ID'])
                            dic_unorder_nodes[dic_case[x]['ID']] = dic_case[x]['str_begin']
                            #print(dic_case[x]['ID'])
                        else:
                            g_occur.attr('node', self.dic_normal_node)
                            g_occur.node(dic_case[x]['ID'], label=dic_case[x]['text'],fontname="SimHei")
                            #lst_node.append(dic_case[x]['ID'])
                            dic_unorder_nodes[dic_case[x]['ID']] = dic_case[x]['str_begin']
                            #print(dic_case[x]['str_begin'])
            if 'hazard_sub' in x:
                    if dic_case[x]["inChain"]:
                        with self.g.subgraph(name='cluster_1') as g_hazard:
                            g_hazard.attr(color='white', rank='max')
                            g_hazard.attr('node', self.dic_hazard_sub_node)
                            g_hazard.node(dic_case[x]['ID'], label=dic_case[x]['text'], fontname="SimHei")
                            dic_hazrd_sub[dic_case[x]['ID']] = dic_case[x]['target']
            if 'atrisk' in x:
                    if dic_case[x]["inChain"]:
                        with self.g.subgraph(name='cluster_2') as g_atrisk:
                            g_atrisk.attr(color='white', rank='max')
                            g_atrisk.attr('node', self.dic_atrisk_node)
                            g_atrisk.node(dic_case[x]['ID'], label=dic_case[x]['text'], fontname="SimHei")
                            dic_atrisk[dic_case[x]['ID']] = dic_case[x]['target']
                            # print(dic_atrisk[dic_case[x]['ID']])
                            # print('====')


        #按照occur出现的顺序进行排序
        a = sorted(dic_unorder_nodes.items(), key=lambda x: x[1], reverse=False)
        for y in a:
            lst_node.append(y[0])
        i = 0
        while i < len(lst_node) :
           if i+1 < len(lst_node) :
             self.g.edge(lst_node[i], lst_node[i + 1])
           for z in dic_hazrd_sub:
               if dic_hazrd_sub[z] == dic_unorder_nodes[lst_node[i]]:
                   self.g.edge(z,lst_node[i])
           for q in dic_atrisk:
               if dic_atrisk[q] == dic_unorder_nodes[lst_node[i]]:
                   self.g.edge(lst_node[i],q)
           i = i + 1

        self.g.render(filename='occur_focus_one',view = self.nview)

        return

    def delete_exit_occur_png(self,filename):
        '''删除当前图片'''
        if (os.path.exists(self.png_dir + filename)):
            os.remove(self.png_dir + filename)
            return True
        else:
            return False




if __name__ == '__main__':
     #root = Tk()
    # img = Image.open('..\\temp\occ.gv.png')  # 打开图片
    # photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
    # imglabel = Label(root, image=photo)
    # imglabel.grid(row=0, column=0, columnspan=3)
    # root.mainloop()
     #r = RenderFlow(6,nview=True)
     r = LR_RenderFlow(6, nview=True)
     r.focus_one_occur(251,253)


