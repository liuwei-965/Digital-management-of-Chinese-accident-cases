import xlrd
import json
def factexcel_to_json():
    excel = xlrd.open_workbook(r'C:\Users\正在输入---\Desktop\reason.xlsx')
    jsonfile = open('C:\\Users\\正在输入---\\Desktop\\fact_all.json','w',encoding='utf-8')
    sheet = excel.sheet_by_name('主体标注')   #获得主体标注sheet数据
    cols0 = sheet.col_values(0)   #获取第一列数据 事实
    #cols1 = sheet.col_values(1)  # 获取第二列数据 角色
    cols2 = sheet.col_values(3)  # 获取第四列数据 主体
    cols3 = sheet.col_values(5)  # 获取第六列数据 类别
    cols4 = sheet.col_values(6)  # 获取第七列数据 角色错位的类型
    dic = {}
    facts_list = []
    #print(dir)
    for i in range(len(cols0)):   #去除无用字符
        fact = cols0[i]
        #role_dis = cols1[i]
        stakeholder = cols2[i]
        type = cols3[i]
        role_dis_type = cols4[i]
        ignore_char = ['[', ']', "'",' ']
        for char in ignore_char:
            fact = fact.replace(char, '')
        fact_list = fact.split(',')   #将字符串转换成list
        facts_list.append(fact_list)
        dic["elements"] = fact_list    #将list存放到字典中
        #dic['role_dis'] = role_dis
        dic['stakeholder'] = stakeholder
        dic['type'] = type
        dic['role_dis_type'] = role_dis_type
        json.dump(dic,jsonfile,ensure_ascii=False)    #ensure_ascii=False防止出现乱码情况
        jsonfile.write("\n")   #逐行写入
    #print(dir)
    jsonfile.close()
    return (facts_list,cols2,cols3,cols4)


if __name__ =="__main__":
    print (factexcel_to_json()[0])