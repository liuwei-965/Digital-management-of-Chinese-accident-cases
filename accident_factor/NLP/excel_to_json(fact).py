import xlrd
import json
def excel_to_json():
    excel = xlrd.open_workbook(r'C:\Users\正在输入---\Desktop\reason.xlsx')
    jsonfile = open('C:\\Users\\正在输入---\\Desktop\\fact.json','w',encoding='utf-8')
    sheet = excel.sheet_by_name('主体标注')   #获得主体标注sheet数据
    cols = sheet.col_values(0)   #获取第一列数据
    dic = {}
    #print(dir)
    for fact in cols:   #去除无用字符
        ignore_char = ['[', ']', "'",' ']
        for char in ignore_char:
            fact = fact.replace(char, '')
        fact_list = fact.split(',')   #将字符串转换成list
        dic["elements"] = fact_list    #将list存放到字典中
        json.dump(dic,jsonfile,ensure_ascii=False)    #ensure_ascii=False防止出现乱码情况
        jsonfile.write("\n")   #逐行写入
    #print(dir)
    jsonfile.close()

excel_to_json()