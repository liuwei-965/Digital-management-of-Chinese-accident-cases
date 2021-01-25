from tkinter import *
from PIL import Image, ImageTk
class flowpng():
    # def __init__(self, rt,filename):
    #     rt.update()
    #     self.root = rt
    #     size= rt.winfo_width(),rt.winfo_height()*1.5
    #     img = Image.open(filename)  # 打开图片
    #     # img.thumbnail(size)
    #     photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
    #     # imglabel = Label(rt, image=photo)
    #     # imglabel.image = photo
    #     # imglabel.grid(row=0, column=0)
    #     # scroll_y = Scrollbar(rt)
    #     # scroll_y.config(command=imglabel.yview)
    #     # imglabel.configure(yscrollcommand=scroll_y.set)
    #     # scroll_y.pack(side='right', fill='y')
    #     canv = Canvas(rt, relief=SUNKEN)
    #     canv.config(width=400, height=200)
    #     canv.grid(row=0, column=0)
    #     canv.create_image(0, 0, anchor="nw", image=photo)

    def __init__(self, rt, filename):
        self.canv = Canvas(rt, relief=SUNKEN,bg= 'white')   #创建背景画布,显示图形，（事故链的图形）
        rt.update()
        self.framewidth = rt.winfo_width()
        self.frameheight = rt.winfo_height()
        self.canv.config(width=self.framewidth, height=self.frameheight-50)
        self.canv.config(highlightthickness=0)

        sbarV = Scrollbar(rt, orient=VERTICAL)
        sbarV.config(command=self.canv.yview)
        self.canv.config(yscrollcommand=sbarV.set)
        sbarV.pack(side=RIGHT, fill=Y)

        self.canv.pack(side=TOP, expand=YES, fill=BOTH)
        self.refresh(filename)


    def refresh(self,filename):
        '''更新图片，剪裁保存'''
        im = Image.open(filename)
        im.thumbnail((self.framewidth,self.frameheight*1.5))   #剪裁图片
        width, height = im.size
        self.canv.config(scrollregion=(0, 0, width, height))
        im2 = ImageTk.PhotoImage(im)   #调整图片大小
        self.canv.create_image(0, 0, anchor="nw", image=im2)
        self.canv.image = im2


if __name__ == '__main__':
    root = Tk()
    flowpng(root,'..\\temp\\occur.png')
    root.mainloop()

