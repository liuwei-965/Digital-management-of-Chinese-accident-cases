__author__='Nizj_DUT'
__author__='确定完事故链之后，确定事故链上每一个节点的前因（如果有），和后果（如果有）'
# import sys
# sys.path.append('.\GUI')
# sys.path.append('.\\NLP')

from tkinter import *
from GUI.LR_TextPad import TextPad
from GUI.browser_ButtonGroup import browser_ButtonGroup 
from GUI.flowpng import flowpng
from iniconfig import iniconfig
from GUI.LR_atrisk_buttons import LR_atrisk_buttons 
from GUI.LR_hazardsuj_buttons import LR_hazardsuj_buttons 
from NLP.db_occur_equiz import db_occur_equiz
from NLP.phase_thread import phase_thread


#=====GUI=================

root = Tk(className = "Hazard subjects & Elements at risk")
root.geometry("1200x900")
root.update()
iniconfig = iniconfig()

dbcursor = iniconfig.read_dbcursor()
dbnlp = db_occur_equiz(dbcursor)
# leftframe = Frame(root,width=root.winfo_width()*2/3, height = root.winfo_height())
# rightframe = Frame(root,width=root.winfo_width()*1/3, height = root.winfo_height())

sourceframe = Frame(root,width=root.winfo_width()*2/3, height = root.winfo_height()*1/2)
phaseframe = Frame(root,width=root.winfo_width()*2/3, height = root.winfo_height()/8,bd=2)
operateframe = Frame(root,width=root.winfo_width()*2/3, height = root.winfo_height()/8,bd=2)
browserframe = Frame(root,width=root.winfo_width()*2/3, height = root.winfo_height()/4,relief=SUNKEN,bd=2)
chainframe = Frame(root,width=root.winfo_width()*1/3, height = root.winfo_height())

sourceframe.grid(row=0, column=0,padx=1,pady=3)
phaseframe.grid(row=1, column=0,padx=1,pady=3)
operateframe.grid(row=2, column=0,padx=1,pady=3)
browserframe.grid(row=3, column=0,padx=1,pady=3)
chainframe.grid(row=0, column=1,rowspan=4,padx=1,pady=3)

chain_buttons_frame = LabelFrame(operateframe, text="   hzard subjects   ",width = root.winfo_width()/3,height=root.winfo_height()/8-10,font=("Times", "12", "normal"))
model_buttons_frame = LabelFrame(operateframe, text="   Element @ risk   ",width = root.winfo_width()/3,height=root.winfo_height()/8-10,font=("Times", "12", "normal"))
chain_buttons_frame.grid(row=0, column=0,padx=10,pady=3)
model_buttons_frame.grid(row=0, column=1,padx=10,pady=3)


png = flowpng(chainframe,'.\\temp\occur.png')
textpad = TextPad(dbnlp,png, dbcursor,phaseframe,sourceframe,font=("黑体", 11, "normal"))
browser_ButtonGroup(dbnlp,browserframe,dbcursor,textpad)
LR_hazardsuj_buttons(chain_buttons_frame,textpad)
LR_atrisk_buttons(model_buttons_frame,dbcursor,textpad)



root.mainloop()

