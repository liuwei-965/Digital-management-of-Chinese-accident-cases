__author__='Nizj_DUT'
__author__='确定事故链'
import sys
sys.path.append('.\GUI')
sys.path.append('.\\NLP')

from tkinter import *
from GUI.model_buttons import model_buttons 
from GUI.chain_buttons import chain_buttons 
from GUI.LR_TextPad import TextPad
from GUI.browser_ButtonGroup import browser_ButtonGroup 
from GUI.flowpng import flowpng
from iniconfig import iniconfig
from NLP.db_occur_equiz import db_occur_equiz
#from NLP.phase_thread import phase_thread


#=====GUI=================

root = Tk(className = " Accidents Chain Mining")
root.geometry("1200x900")
root.update()
iniconfig = iniconfig()

dbcursor = iniconfig.read_dbcursor()-1 #获取当前窗口案例的索引
#print(dbcursor)
dbnlp = db_occur_equiz(dbcursor)  #实例化 类db_occur_equiz
#print(dbnlp)
# leftframe = Frame(root,width=root.winfo_width()*2/3, height = root.winfo_height())
# rightframe = Frame(root,width=root.winfo_width()*1/3, height = root.winfo_height())

sourceframe = Frame(root,width=root.winfo_width()*2/3, height = root.winfo_height()*1/2)
phaseframe = Frame(root,width=root.winfo_width()*7/12, height = root.winfo_height()/8,bd=2)  #整个左侧内容
operateframe = Frame(root,width=root.winfo_width()*2/3, height = root.winfo_height()/8,bd=2)
browserframe = Frame(root,width=root.winfo_width()*2/3, height = root.winfo_height()/4,relief=SUNKEN,bd=2)
chainframe = Frame(root,width=root.winfo_width()*1/3, height = root.winfo_height())

sourceframe.grid(row=0, column=0,padx=1,pady=3)
phaseframe.grid(row=1, column=0,padx=1,pady=3)
operateframe.grid(row=2, column=0,padx=1,pady=3)
browserframe.grid(row=3, column=0,padx=1,pady=3)
chainframe.grid(row=0, column=1,rowspan=4,padx=1,pady=3)

chain_buttons_frame = LabelFrame(operateframe, text="   To Chain   ",width = root.winfo_width()/3,height=root.winfo_height()/8-10,font=("Times", "12", "normal"))
model_buttons_frame = LabelFrame(operateframe, text="   To Model   ",width = root.winfo_width()/3,height=root.winfo_height()/8-10,font=("Times", "12", "normal"))
chain_buttons_frame.grid(row=0, column=0,padx=10,pady=3)
model_buttons_frame.grid(row=0, column=1,padx=10,pady=3)

#.\\temp\occur.png
# png = flowpng(chainframe,'C:\\Users\\正在输入---\\Desktop\\chain_finder\\temp\\occur_focus_one.png')
png = flowpng(chainframe,'.\\temp\occur.png')
textpad = TextPad(dbnlp,png,dbcursor,phaseframe,sourceframe,font=("黑体", 11, "normal"))
#textpad = TextPad(dbnlp,dbcursor,phaseframe,sourceframe,font=("黑体", 11, "normal"))
browser_ButtonGroup(dbnlp,browserframe,dbcursor,textpad)   #下方换页控件
chain_buttons(chain_buttons_frame,textpad)    #链按钮
model_buttons(model_buttons_frame,dbcursor,textpad)     #模型按钮

root.mainloop()

