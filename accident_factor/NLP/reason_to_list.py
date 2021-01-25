from pymongo import MongoClient
from collections import defaultdict
import xlsxwriter



def reason_to_list():
    myclient = MongoClient('mongodb://localhost:27017/')
    mydb = myclient["高空坠落事故坠落"]
    test_collection = mydb["fall 119"]
    fall_cases = test_collection.find({})
    #遍历每一个案例
    for case in fall_cases:
        for reason in case['间接原因']:
            reason_list = reason.split('\n')
            while  '\t' in reason_list:
                reason_list.remove('\t')
            while  '\r' in reason_list:
                reason_list.remove('\r')
            while '' in reason_list:
                reason_list.remove('')
        test_collection.update_one({"_id": case['_id']},
                                            {'$set': {'间接原因': reason_list}})
    #print(reason_list)


if __name__ =="__main__":
    role_dis_model()
