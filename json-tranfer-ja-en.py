
#!/usr/bin/env python

import json
import sys
import xlsxwriter

exel_file = sys.argv[3]
array_parent_en = []
array_parent_ja = []
array_en = []
array_ja = []

def enumerate_ja(obj_ja, layer, parent):

    if(isinstance(obj_ja, list)):
        for i in range(0, len(obj_ja)):
            enumerate_ja(obj_ja[i], layer+1, parent + "/" + str(i))

    elif(isinstance(obj_ja, dict)):
        for key in obj_ja.keys():
            enumerate_ja(obj_ja[key], layer+1, parent + "/" + key)

    else:
        array_parent_ja.append(parent)
        array_ja.append(obj_ja)

def enumerate_en(obj_en, layer, parent):

    if(isinstance(obj_en, list)):
        for i in range(0, len(obj_en)):
            enumerate_en(obj_en[i], layer+1, parent + "/" + str(i))

    elif(isinstance(obj_en, dict)):
        for key in obj_en.keys():
            enumerate_en(obj_en[key], layer+1, parent + "/" + key)

    else:
        # print parent, "|", obj_ja
        array_parent_en.append(parent)
        array_en.append(obj_en)

def save_to_xlsx(exel_file):
    print "leng of index: ", len(array_en)
    print "leng of index: ", len(array_ja)
    
    workbook = xlsxwriter.Workbook(exel_file)
    worksheet = workbook.add_worksheet()
    for index in range(0,len(array_parent_en)):
        if(array_parent_en[index] != array_parent_ja[index]): 
            print "Different line: ", index
            print "array_en", array_en[index]
            worksheet.write(index, 4, "Different")
            worksheet.write(index, 2, find_ja(index))
            


        worksheet.write(index, 0, array_parent_en[index]) #column 0 - english route
        worksheet.write(index, 2, array_en[index]) #column 1 - english word
        worksheet.write(index, 1, array_parent_ja[index]) #column 1 - japanese route
        worksheet.write(index, 3, array_ja[index]) #column 2 - japanese word
        print array_parent_en[index], ":", array_en[index], ":", array_ja[index]
    workbook.close()

def find_ja(index):
    index = array_parent_ja.index(array_parent_en[index])
    print "array_ja", array_ja[index]
    return array_ja[index]

if __name__ == '__main__':

    if len(sys.argv) != 4 :
        print "Usage: %spython [json-tranfer-ja-en.py] [en_json file name] [ja_json file name] [xlsx file name]" % sys.argv[0]
        exit(1)

    f = open(sys.argv[1], 'r')
    obj_en = json.load(f)
    f.close()

    f2 = open(sys.argv[2], 'r')
    obj_ja = json.load(f2)
    f2.close()

    enumerate_en(obj_en, 0, "      ")
    enumerate_ja(obj_ja, 0, "      ")

    save_to_xlsx(exel_file)


