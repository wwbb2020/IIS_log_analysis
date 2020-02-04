import requests
from bs4 import BeautifulSoup
import time


def get_ip_region(IP_address):
    url='http://m.ip138.com/ip.asp?ip='

    try:
        r=requests.get(url+IP_address)
        r.raise_for_status()
        wb_bs=BeautifulSoup(r.text,'html.parser')
        tag1=wb_bs.h1
        tag2=tag1.next_sibling
        # tag3=tag2.next_sibling
        # print(tag1.string,tag2.string,tag3.string,)
        str=tag2.string[6:]
    except:
        # print('爬取不成功啊！')
        str='未知来源'
    return str

def list_add(list_1,list_2,ignore_fileds=0):
    if len(list_1)!=len(list_2):
        return 0
    for i in range(ignore_fileds,len(list_1)):
        list_1[i]=list_1[i]+list_2[i]
    return list_1

def is_page(str):
    if str[-1]=='/' or str[-3:].upper()=='HTM' or \
            str[-4:].upper()=='HTML':
        return 1
    return 0

def is_file(str):
    if '.' in str[-5:] and not is_page(str):
        return 1
    return 0

def is_session(date,time1,time2):
    if time2=='00':
        return 1

    timeArray1 = time.strptime(date + " " + time1, "%Y-%m-%d %H:%M:%S")
    timeStamp1 = int(time.mktime(timeArray1))
    timeArray2 = time.strptime(date + " " + time2, "%Y-%m-%d %H:%M:%S")
    timeStamp2 = int(time.mktime(timeArray2))
    if abs(timeStamp1-timeStamp2)>600:
        return 1
    return 0

def is_error(str):
    if str != '200' and str != '304':
        return 1
    return 0

def chang_list_to_string(userlist):
    strlist = [str(j) for j in userlist]
    wstr=','.join(strlist)
    return wstr

def chang_row_to_string(userrow):  #估计本方法用不到了，类型不对，rows是字典
    wstr=userrow[0]+','+chang_list_to_string(userrow[1])
    return wstr

def line_to_row(line,last_time):
    IP_Address=line[8]
    line_date=line[0]
    line_time=line[1]
    visit_number=1
    line_session=is_session(line_date,line_time,last_time)
    line_page=is_page(line[4])
    line_file=is_file(line[4])

    # if (not is_page(line[4])) and  (not is_file(line[4])):
    #     print("这个URL有点异常：{}".format(line[4]))

    line_time_taken=eval(line[13])
    line_error=is_error(line[10])
    return {IP_Address:[line_date,line_time,line_session,\
                        visit_number,line_page,line_file,line_time_taken,line_error]}



if __name__ == "__main__":
    # list1=['1','2','3','4','5']
    # list2=['2','2','2','2','2']
    # l3=list_add(list1,list2,3)
    # print(l3)

    # print(get_ip_region('159.131.1.3'))
    # print('lallala')
    # print(get_ip_region('115.171.112.36'))
    # print('dfsjsf')
    # print(get_ip_region('59.162.1.1'))
    # print('unnn------------end')

    # print(chang_row_to_string(('1.1.1.1',[1,2,3,4.56,'ghtghhh'])))
    print(is_session('2019-12-11','00:00:02','00:00:08'))
    print(is_session('2019-12-11', '00:00:02', '00:10:01'))
    print(is_session('2019-12-11', '00:00:02', '00:10:02'))
    print(is_session('2019-12-11', '00:00:02', '00:10:03'))
    print(is_session('2019-12-11', '00:00:02', '01:10:01'))



