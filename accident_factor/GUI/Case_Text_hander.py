import sys
import tkinter

sys.path.append('.\GUI')
sys.path.append('..\\NLP')

from NLP.db_occur_equiz import db_occur_equiz
from GUI.RenderFlow import RenderFlow

class Texthander():
    import tkinter

    def __init__(self, text,obj_id):
        self.text = text
        self.click_tag_begin = 0
        self.click_tag_end = 0
        self.obj_id = obj_id
        self.r = RenderFlow(obj_id)

        self.text.tag_bind("occur", '<Button-1>',self._occur_click)


    def _occur_click(self,event):
        #get the index of the mouse click
        click_index = float(event.widget.index("@%s,%s" % (event.x, event.y)))
        print("="*20)
        # get the indices of all "occur" tags
        tag_indices = list(event.widget.tag_ranges('occur'))
        i = 0

        for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
            # check if the tag matches the mouse click index
            if event.widget.compare(start, '<=', click_index) and event.widget.compare(click_index, '<', end):
                # return string between tag start and end
                self.click_tag_begin = int(str(start)[2:])
                self.click_tag_end = int(str(end)[2:])
        self.r.focus_one_occur(self.click_tag_begin,self.click_tag_end)


if __name__ == '__main__':
    root = tkinter.Tk()
    pad = tkinter.Text(root)
    pad.pack()
        # self.text.insert('1.0','我是大坏蛋，哈哈哈哈，无聊死了，存储罐。')
        # self.text.tag_add('occur','1.3','1.6')
        # self.text.tag_add('occur','1.8','1.9')
        # self.text.tag_configure("occur", background="skyblue", foreground="red")
    Texthander(pad)
    root.mainloop()