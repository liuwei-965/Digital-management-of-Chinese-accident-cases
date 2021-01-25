import sys
sys.path.append('.\GUI')
sys.path.append('..\\NLP')
sys.path.append('..\\temp')

import os
os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz2.38/bin/'

from NLP.db_occur_equiz import db_occur_equiz
from graphviz import Digraph

class RenderFlow():
    def __init__(self, dbcursor,db,nview=False):
        self.db = db_occur_equiz(dbcursor)
        self.objid = self.db.getcurrent_objid()
        self.dic_normal_node ={'shape':'egg','style':'radial','fillcolor':'white:lightblue'}
        self.dic_focus_one_node ={'shape':'egg','style':'radial','fillcolor':'white:red'}
        self.nview = nview
        #self.objid = dbcursor
        if __name__ == '__main__':
            self.png_dir = '../temp/'
        else:
            self.png_dir = './temp/'
        self.g = Digraph('test_occur_graphviz', directory=self.png_dir, format='png')
        self.renderWhole()


    def renderWhole(self):
        self.delete_exit_occur_png('occur.png')
        dic_case = self.db.getOneCase(self.objid)
        lst_node = []
        dic_unorder_nodes = {}

        self.g.clear()

        for x in dic_case:
            if 'occur' in x:
                if dic_case[x]["inChain"]:
                    self.g.attr('node', self.dic_normal_node)
                    self.g.node(dic_case[x]['ID'], label=dic_case[x]['text'],fontname="SimHei")
                    dic_unorder_nodes[dic_case[x]['ID']] = dic_case[x]['str_begin']
            i = 0
        #按照occur出现的顺序进行排序
        a = sorted(dic_unorder_nodes.items(), key=lambda x: x[1], reverse=False)
        for y in a:
            lst_node.append(y[0])
        while i < len(lst_node) - 1:
           self.g.edge(lst_node[i], lst_node[i + 1])
           i = i + 1
        self.g.render(filename='occur')


    def focus_one_occur(self,click_index):
        self.delete_exit_occur_png('occur_focus_one.png')
        dic_case = self.db.getOneCase(self.objid)
        lst_node = []
        dic_unorder_nodes = {}

        self.g.clear()

        for x in dic_case:
            if 'occur' in x:
                #如果被选中
                if dic_case[x]["inChain"]:
                    if dic_case[x]['str_begin'] <= click_index and dic_case[x]['str_end'] >= click_index:
                        self.g.attr('node', self.dic_focus_one_node)
                        self.g.node(dic_case[x]['ID'], label=dic_case[x]['text'],fontname="SimHei")
                        #lst_node.append(dic_case[x]['ID'])
                        dic_unorder_nodes[dic_case[x]['ID']] = dic_case[x]['str_begin']
                        #print(dic_case[x]['ID'])
                    else:
                        self.g.attr('node', self.dic_normal_node)
                        self.g.node(dic_case[x]['ID'], label=dic_case[x]['text'],fontname="SimHei")
                        #lst_node.append(dic_case[x]['ID'])
                        dic_unorder_nodes[dic_case[x]['ID']] = dic_case[x]['str_begin']
                        #print(dic_case[x]['str_begin'])
            i = 0
        #按照occur出现的顺序进行排序
        a = sorted(dic_unorder_nodes.items(), key=lambda x: x[1], reverse=False)
        for y in a:
            lst_node.append(y[0])
        while i < len(lst_node) - 1:
           self.g.edge(lst_node[i], lst_node[i + 1])
           i = i + 1

        self.g.render(filename='occur_focus_one',view = self.nview)

        return

    def delete_exit_occur_png(self,filename):
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
     r = RenderFlow(6,nview=True)
     r.focus_one_occur(251,253)


