from pymongo import MongoClient
from collections import defaultdict
import xlsxwriter



def role_dis_model():
    myclient = MongoClient('mongodb://localhost:27017/')
    mydb = myclient["高空坠落事故坠落"]
    test_collection = mydb["role_dislocation"]
    db_verb_types = mydb["facts"]

    role_dislocations = test_collection.find({})
    verb_types = db_verb_types.find({})
    role_dis_dic = defaultdict(list)
    role_dis_statistics = {}  #角色错位类别的统计情况
    model =[]
    numbers =[]
    #遍历每一个案例
    for role_dislocation in role_dislocations:
        #遍历每一个案例中的角色错位类别
        for role_dis in role_dislocation['role_dis_types']:
            #将案例原因类别加入到角色错位的字典中
            role_dis_dic [role_dis ].extend(role_dislocation['types'])

    #统计频率
    #遍历每一个角色错位类别
    for role_dis in role_dis_dic:
        role_dis_stics = {}
        #遍历一类角色错位中的案例原因
        for i in role_dis_dic[role_dis]:
            if i not in role_dis_stics:
                role_dis_stics[i] = 1
            else:
                role_dis_stics[i] +=1
        role_dis_statistics[role_dis] = role_dis_stics

    #将统计情况按照value值进行排序输出
    for role_dis_stics in role_dis_statistics:
        type_num = 0
        for case in test_collection.find({'role_dis_types': {"$regex": role_dis_stics}}):
            type_num += 1
        a = sorted(role_dis_statistics[role_dis_stics].items(),key = lambda x:x[1],reverse = True)
        model.append(a)
        numbers.append(type_num)
        print("角色错位类别为：%s\t出现在 %d 个案例中\n%s\n" %(role_dis_stics,type_num,str(a)))
    #print(type(test_collection.find({'role_dis_types': {'RegExp': role_dis_stics}})))
    return (model,role_dis_statistics,numbers)


def model_to_excel(model,role_dis_statistics,numbers):
    workbook = xlsxwriter.Workbook('model.xlsx')  # 创建一个excel文件
    worksheet = workbook.add_worksheet(u'sheet1')  # 在文件中创建一个名为TEST的sheet,不加名字默认为sheet1
    for i,v in enumerate(role_dis_statistics):
        worksheet.write(0,i * 2,v)
        worksheet.write(0, i * 2 + 1, numbers[i])
    for i,v in enumerate(model):
            for r,w in enumerate(v):
                worksheet.write(r+1, i * 2, w[0])
                worksheet.write(r+1, i * 2 + 1, w[1])
    workbook.close()
    return

if __name__ =="__main__":
    model,role_dis_statistics,numbers =role_dis_model()
    model_to_excel(model,role_dis_statistics,numbers)
