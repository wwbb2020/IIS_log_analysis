import csv
import makerow
import sys
import os
from datetime import datetime

def get_log_content(file_name):
    rows = {}
    url_dict={}

    # with open('E:/Office/2020/外网网站/W3SVC1-2019网站日志/u_ex191227.log', 'r', encoding='gb18030', errors='ignore')  as csvfile:
    with open(file_name, 'r', encoding='gb18030', errors='ignore')  as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')

        print('开始读文件')
        i = 0
        for line in reader:
            i += 1
            if i > 4:
                IP_ADD = line[8]
                last_log=rows.get(IP_ADD,['','00',0,0,0,0,0,0]) #'00'为session计算判断以前没记录，与'00:00:00'相区别
                last_time=last_log[1]
                row=makerow.line_to_row(line,last_time)
                new_row_value=makerow.list_add(row[IP_ADD],last_log,2)
                rows[IP_ADD]=new_row_value
                url_str=line[4]
                url_dict[url_str] = url_dict.get(url_str, 0) + 1
                if  i%100000==0:
                    print('已读取{}条记录'.format(i))
        csvfile.close()
    return rows,url_dict

def add_IP_region(rows):
    key_num=0
    print('开始查找IP所属区域')
    for key in rows:
        key_num+=1
        if key_num%100==0:
            print('已经查询{}条地址'.format(key_num))

        # 得到IP所属区域并加入列表
        region=makerow.get_ip_region(key)
        rows[key].append(region)
    return rows

def summary_IP(rows):
    row_date = ''
    row_time = ""
    num_session = 0
    num_visit = 0
    num_page = 0
    num_file = 0
    num_seconds = 0
    num_errors = 0
    # row_region = '汇总信息'
    key_num = 0
    print('开始汇总访问主站的IP信息')
    for key in rows:
        key_num += 1
        # if key_num % 5000 == 0:
        #     print('已经查询{}条地址'.format(key_num))
        if key_num == 1:
            row_date = rows[key][0]
        # 计算统计汇总值
        values = rows[key]
        num_session += values[2]
        num_visit += values[3]
        num_page += values[4]
        num_file += values[5]
        num_seconds += values[6]
        num_errors += values[7]
    rows['0.0.0.0'] = [row_date, row_time, num_session, num_visit, \
                       num_page, num_file, num_seconds, num_errors, '汇总信息共' + str(key_num) + '条']
    return rows

def write_rows_to_file(file_name,rows):
    # with open('E:/Office/2020/外网网站/W3SVC1-2019网站日志/191227.ana.csv', 'w')  as logfile:
    with open(file_name, 'w')  as logfile:
        print('开始写IP汇总信息到指定文件{}'.format(file_name))

        logfile.write('IP,date,time,session,visit,pages,files,seconds,errors,region')
        logfile.write('\n')

        for key in rows:
            line=key+','+makerow.chang_list_to_string(rows[key])
            logfile.write(line)
            logfile.write('\n')

        logfile.close()

def write_sum_info_to_file(file_name,rows,url_dict):

    line = makerow.chang_list_to_string(rows['0.0.0.0'])
    line=line.replace('汇总信息共','')
    line = line.replace('条', '')
    line = line.replace(',,', ',',1)
    line_url=anz_url_log('',url_dict)
    line=line+','+line_url
    line=line+get_first_five_ip(rows)
    print(line)

    with open(file_name, 'a')  as logfile:
        print('开始写IP汇总信息到指定文件{}'.format(file_name))
        logfile.write(line)
        logfile.write('\n')

        logfile.close()



def anz_url_log(file_name,url_dict,number=100,min_time=0):
    items = list(url_dict.items())
    items.sort(key=lambda x: x[1], reverse=True)
    count = len(items)

    if file_name=='':
        #如果没有指定文件，则返回访问量前五名的url和次数，用于汇总记录
        url_str=''
        for i in range(5):
            url, count1 = items[i]
            url_str=url_str+','+str(url)+','+str(count1)
        return  url_str[1:]

    with open(file_name, 'a')  as anzfile:
        print('——————————————————————————————————————————————————————————————————————————————')
        print('开始记录URL分析结果，前{}名或超过{}次的记录'.format(number, min_time))
        print("***************************************************************************************")
        print('——————————————————————————————————————————————————————————————————————————————',file=anzfile)
        print('开始记录URL分析结果，前{}名或超过{}次的记录'.format(number, min_time),file=anzfile)
        print("***************************************************************************************",file=anzfile)

        if min_time==0:
            for i in range(number):
                url, count1 = items[i]
                print("本日访问数第{}多的页面/文件是{}，共被访问{:,}次".format(i+1,url, count1))
                print("本日访问数第{}多的页面/文件是{}，共被访问{:,}次".format(i + 1, url, count1),file=anzfile)
            print('**************************************************')
            print("本日总共有{:,}个页面/文件被访问".format(count))
            print('**************************************************',file=anzfile)
            print("本日总共有{:,}个页面/文件被访问".format(count),file=anzfile)
        else:
            for i in range(count):
                url, count1 = items[i]
                if count1<min_time:
                    break
                print("本日访问数第{}多的页面/文件是{}，共被访问{:,}次".format(i + 1, url, count1))
                print("本日访问数第{}多的页面/文件是{}，共被访问{:,}次".format(i + 1, url, count1),file=anzfile)
            print('**************************************************')
            print("本日总共有{:,}个页面/文件被访问".format(count))
            print('**************************************************',file=anzfile)
            print("本日总共有{:,}个页面/文件被访问".format(count),file=anzfile)
    anzfile.close()

def anz_ip_rows(file_name,rows,key,describe,number=100,min_time=0):
    items = list(rows.items())
    items.sort(key=lambda x: x[1][key], reverse=True)

    count = len(items)
    sum_of_key=-1


    if min_time==0:
        for_number=number
    else:
        for_number=count

    with open(file_name, 'a')  as anzfile:
        print("————————————————————————————————————————————————————————————————————————————————————————————————————")
        print("{}的次数排序结果，前{}名或超过{}次的记录".format(describe, number,min_time))
        print("***************************************************************************************")
        print("————————————————————————————————————————————————————————————————————————————————————————————————————",file=anzfile)
        print("{}的次数排序结果，前{}名或超过{}次的记录".format(describe, number, min_time),file=anzfile)
        print("***************************************************************************************",file=anzfile)
        for i in range(for_number+1):
            IP_add, counts = items[i]

            if counts[key]<min_time:
                    break

            if len(counts)>8:
                IP_region =counts[8]
            else:
                IP_region = '尚未查询地址来源'

            if IP_add=='0.0.0.0':
                sum_of_key=counts[key]
                continue
            print("本日{}第{}多的IP地址是{}（{}），共有{:,}次".format(describe,i,IP_add, IP_region,counts[key]))
            print("本日{}第{}多的IP地址是{}（{}），共有{:,}次".format(describe,i,IP_add, IP_region,counts[key]),file=anzfile)
        print("***************************************************************************************")
        print("本日{}共有{:,}个IP，总共发生{}的次数为：{:,}\n\n".format(describe,count,describe,sum_of_key))
        print("***************************************************************************************",file=anzfile)
        print("本日{}共有{:,}个IP，总共发生{}的次数为：{:,}\n\n".format(describe,count,describe,sum_of_key),file=anzfile)
    anzfile.close()

def get_first_five_ip(rows):
    items = list(rows.items())
    line_str=''

    # 判断循环次数，避免不足五个IP的情况
    count = len(items)
    if count<5:
        for_number=count
    else:
        for_number=5

    ip_rows_value_describe={'日期':0,'最后访问时间':1,'会话数':2,'访问次数':3,'访问页面数':4,\
                             '访问文件数':5,'响应总时长（秒）':6,'错误数':7,'所属区域':8}
    write_key_range=(2,3,4,5,6,7)
    for desc,key in ip_rows_value_describe.items():
        # 挨个排序后处理

        # 排序
        if key in write_key_range:
            items.sort(key=lambda x: x[1][key], reverse=True)
            #排序后开始输出前五名

            #跳过第一行，因为要排除第一行汇总行'0.0.0.0'
            for i in range(1,for_number+1):
                if len(items[i][1]) > 8:
                    IP_region = items[i][1][8]
                else:
                    IP_region = '尚未查询地址来源'

                line_str = line_str + ','+items[i][0]+','+str(items[i][1][key]) \
                        + ',' + IP_region

            # 不足五个时补齐五个
            if count < 5:
                for i in range(count,5):
                    line_str=line_str+',,,'

    return line_str

def get_all_file_names():
    path=os.getcwd()
    dirs=os.listdir(path)
    ls_file_name=[]
    for file_name in dirs:
        if file_name[-4:]=='.log':
            full_name=os.path.join(path,file_name)
            ls_file_name.append(full_name)
    # ls_file_name.sort(reverse=True)
    ls_file_name.sort()
    return ls_file_name

def get_last_filename():
    path = os.getcwd()
    dirs = os.listdir(path)
    ls_file_name = []
    for file_name in dirs:
        if file_name[-4:] == '.log':
            full_name = os.path.join(path, file_name)
            ls_file_name.append(full_name)
    ls_file_name.sort(reverse=True)
    return ls_file_name[1]

def init_out_files():
    # 创建目录analysis
    dirs = 'analysis'
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    # 创建汇总信息文件analysis/all_sum.csv并写入表头
    filename = 'analysis/all_sum.csv'
    if not os.path.exists(filename):
        with open(filename, 'a')  as anzfile:
            title="日期,总会话数,总访问次数,网页访问次数,文件访问次数,总响应秒数,错误数,IP数量,"
            title+='最多访问URL,访问次数,第二url,次数,第三url,次数,第四url,次数,第五url,次数,'
            title+='会话最多IP,次数,地址来源,会话第二IP,次数,地址来源,会话第三IP,次数,地址来源,会话第四IP,次数,地址来源,会话第五IP,次数,地址来源,'
            title+='访问最多IP,次数,地址来源,访问第二IP,次数,地址来源,访问第三IP,次数,地址来源,访问第四IP,次数,地址来源,访问第五IP,次数,地址来源,'
            title+='访问页面最多IP,次数,地址来源,访问页面第二IP,次数,地址来源,访问页面第三IP,次数,地址来源,访问页面第四IP,次数,地址来源,访问页面第五IP,次数,地址来源,'
            title+='访问文件最多IP,次数,地址来源,访问文件第二IP,次数,地址来源,访问文件第三IP,次数,地址来源,访问文件第四IP,次数,地址来源,访问文件第五IP,次数,地址来源,'
            title+='响应时长最多IP,秒数,地址来源,响应时长第二IP,秒数,地址来源,响应时长第三IP,秒数,地址来源,响应时长第四IP,秒数,地址来源,响应时长第五IP,秒数,地址来源,'
            title+='错误最多IP,错误数,地址来源,错误第二IP,错误数,地址来源,错误第三IP,错误数,地址来源,错误第四IP,错误数,地址来源,错误第五IP,错误数,地址来源'
            print(title, file=anzfile)
            anzfile.close()

def main():
    init_out_files()

    ls_file_name=[]
    if len(sys.argv)>1:
        if sys.argv[1]=='*':
            ls_file_name=get_all_file_names()
        elif sys.argv[1]=='-h' or sys.argv[1]=='-H':
            print('-h for help')
            print('* for all *.log file in this dir')
            print('no arg will analysis the last log file in this dir')
            print('汇总信息文件analysis/all_sum.csv')
            print('每日分析文件也在analysis目录下')
            return
        else:
            ls_file_name=sys.argv[1:]
    else:
        ls_file_name.append(get_last_filename())
            # 'E:/Office/2020/外网网站/W3SVC1-2019网站日志/u_ex191227.log'
    rows = {}
    url_dict = {}

    t0 = datetime.now()
    file_numbers=len(ls_file_name)

    for file_name in ls_file_name:
        print(file_name)
        t1= datetime.now()
        rows,url_dict=get_log_content(file_name)
        t2= datetime.now()

        rows=add_IP_region(rows)
        t3= datetime.now()

        rows=summary_IP(rows)
        t4= datetime.now()

        position=file_name.rfind('\\')
        if position==-1:
            position=0
        rowfilename = 'analysis/'+file_name[position:-4]+'_IP.csv'
        write_rows_to_file(rowfilename,rows)

        t5=datetime.now()

        print('读取文件内容共用了{}秒'.format((t2-t1).seconds))
        print('查询IP所属区域共用了{}秒'.format((t3 - t2).seconds))
        print('计算汇总信息共用了{}秒'.format((t4-t3).seconds))
        print('写入汇总文件共用了{}秒'.format((t5 - t4).seconds))



        anzfilename =  'analysis/'+file_name[position:-4]+'_anz.log'
        anz_url_log(anzfilename,url_dict, min_time=500)
        # sum_str=anz_url_log('',url_dict)
        # print(sum_str)

        ip_rows_value_describe={'日期':0,'最后访问时间':1,'会话数':2,'访问次数':3,'访问页面数':4,\
                                 '访问文件数':5,'响应总时长（秒）':6,'错误数':7,'所属区域':8}
        write_key_range=(2,3,4,5,6,7)
        for desc,key in ip_rows_value_describe.items():
            if key in write_key_range:
                anz_ip_rows(anzfilename,rows, key, desc)



        filename = 'analysis/all_sum.csv'
        write_sum_info_to_file(filename,rows,url_dict)

    t11= datetime.now()
    print('总共处理{}个文件共用了{:,}秒'.format(file_numbers,(t11 - t0).seconds))

if __name__ == "__main__":
    main()