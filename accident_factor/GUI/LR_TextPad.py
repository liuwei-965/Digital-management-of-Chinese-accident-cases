from tkinter import *
from GUI.LR_RenderText import LR_RenderText
from GUI.browser_ButtonGroup import browser_ButtonGroup
from GUI.LR_RenderFlow import LR_RenderFlow
from NLP.db_occur_equiz import db_occur_equiz
#from NLP.phase_thread import phase_thread


class TextPad(Text):
	def __init__(self, dbnlp,flowpng,dbcursor,phaseframe,*args, **kwargs):
	#def __init__(self, dbnlp, dbcursor, phaseframe, *args, **kwargs):
		Text.__init__(self, *args, **kwargs)
		self.flowpng =flowpng   #链图
		Scrollbar(self)  #滚动条
		self.phaseframe = phaseframe
		# self.phase_thread = phase_thread(phaseframe,'phase1','hah',1)
		# self.phase_thread.start()
		self.storeobj = {}
		self.dbcursor = dbcursor  #页码
		self.db = dbnlp
		self.Connect_External_Module_Features()
		self.isfocus = False
		self.bindevent()
		self._pack()
		self.occur_clickindex = 0


	def Connect_External_Module_Features(self):
		'''当前显示内容'''
		self.current_objid = self.db.getcurrent_objid()    #获取当前id
		self.rendertext = LR_RenderText(self,self.dbcursor,self.db)  #文本框
		self.r = LR_RenderFlow(self.dbcursor,self.db,False)   #链图内容
		self.flowpng.refresh('.\\temp\occur.png')   #当前链图
		return

	def bindevent(self):
		self.tag_bind("occur1", '<Button-1>', self._occur_click)
		self.tag_bind("occur2", '<Button-1>', self._occur_click)
		self.tag_bind("hazard1", '<Button-1>', self._hazsub_eleATrisk_click)
		self.tag_bind("hazard2", '<Button-1>', self._hazsub_eleATrisk_click)
		# self.tag_bind("occur1", '<Button-2>', self._occur_middle_click)
		# self.tag_bind("occur2", '<Button-2>', self._occur_middle_click)


	def _pack(self):
		self.pack(expand = True, fill = "both")
		return

	def refreshflow(self):
		print(self.dbcursor)

	def _judgephase(self,event):
		click_index = float(event.widget.index("@%s,%s" % (event.x, event.y)))
		self.r.focus_one_occur(int(str(click_index)[2:]))
		#self.flowpng.refresh('.\\temp\occur_focus_one.png')
		#self.phase_thread.get_twoside_phase_score(self.dbcursor,int(str(click_index)[2:]))


	def _hazsub_eleATrisk_click(self, event):
		self.tag_delete('hazard1')
		self.tag_delete('hazard2')
		click_index = float(event.widget.index("@%s,%s" % (event.x, event.y)))
		self.isfocus = True
		#被选中的词在整篇文档中的位置
		self.focus_index = int(str(click_index)[2:])


	def _occur_click(self, event):
		click_tag_begin = 0
		click_tag_end = 0
		# get the index of the mouse click
		click_index = float(event.widget.index("@%s,%s" % (event.x, event.y)))

		self.isfocus = True
		#被选中的词在整篇文档中的位置
		self.focus_index = int(str(click_index)[2:])
		print('%s 你已选中索引' % self.textpad.focus_index)
		self.occur_clickindex = self.focus_index

		self.r.focus_one_occur(self.occur_clickindex)
		self.rendertext.focus_one_occur(self.occur_clickindex,self.dbcursor)
		# print(click_tag_begin)
		# print(click_tag_end)
		#self.flowpng.refresh('.\\temp\occur_focus_one.png')
		self._judgephase(event)
		return

if __name__ == '__main__':
	root = Tk(className = " Test TextPad")
	TextPad(root)
	root.mainloop()