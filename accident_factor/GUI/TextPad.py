from tkinter import *
from GUI.RenderText import RenderText
from GUI.RenderFlow import RenderFlow
from NLP.db_occur_equiz import db_occur_equiz
from NLP.phase_thread import phase_thread


class TextPad(Text):
	def __init__(self, dbnlp,flowpng,dbcursor,phaseframe,*args, **kwargs):
		Text.__init__(self, *args, **kwargs)
		self.flowpng =flowpng
		Scrollbar(self)
		self.phaseframe = phaseframe

		self.phase_thread = phase_thread(phaseframe,'phase1','hah',1)
		self.phase_thread.start()


		self.storeobj = {}
		self.dbcursor = dbcursor
		self.db = dbnlp
		self.Connect_External_Module_Features()
		self.isfocus = False
		self.bindevent()
		self._pack()

	def Connect_External_Module_Features(self):
		self.current_objid = self.db.getcurrent_objid()
		RenderText(self,self.dbcursor,self.db)
		self.r = RenderFlow(self.dbcursor,self.db,False)
		self.flowpng.refresh('.\\temp\occur.png')
		return

	def bindevent(self):
		self.tag_bind("occur1", '<Button-1>', self._occur_click)
		self.tag_bind("occur2", '<Button-1>', self._occur_click)
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
		self.flowpng.refresh('.\\temp\occur_focus_one.png')
		self.phase_thread.get_twoside_phase_score(self.dbcursor,int(str(click_index)[2:]))



	def _occur_click(self, event):
		click_tag_begin = 0
		click_tag_end = 0
		# get the index of the mouse click
		click_index = float(event.widget.index("@%s,%s" % (event.x, event.y)))
		print("=" * 20)
        # get the indices of all "occur" tags
		# tag_indices = list(event.widget.tag_ranges('occur'))
		# #print(tag_indices)
		#
		# for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
		# 	#check if the tag matches the mouse click index
		# 	if event.widget.compare(start, '<=', click_index) and event.widget.compare(click_index, '<', end):
        #     #return string between tag start and end
		# 		click_tag_begin = int(str(start)[2:])
		# 		click_tag_end = int(str(end)[2:])
		# 		print(click_index)
				# print(start)
				# print(end)
		self.isfocus = True
		#被选中的词在整篇文档中的位置
		self.focus_index = int(str(click_index)[2:])

		self.r.focus_one_occur(self.focus_index)
		# print(click_tag_begin)
		# print(click_tag_end)
		self.flowpng.refresh('.\\temp\occur_focus_one.png')
		self._judgephase(event)
		return

if __name__ == '__main__':
	root = Tk(className = " Test TextPad")
	TextPad(root)
	root.mainloop()