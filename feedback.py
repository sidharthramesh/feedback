import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from multiprocessing import Pool, cpu_count
import pandas as pd

def main(username, password, rating=5):
    
    url = "https://feedback.manipal.edu/sfdfacultyfeedback/login_stud.aspx"
    service_url = "https://feedback.manipal.edu/Services_Feedback/login_mpl.aspx"
    print("[+] For {}".format(username))
    dr = webdriver.Firefox()

    def login(username=username, password=password):
        dr.get(url)
        uname_ele = dr.find_element_by_id("ContentPlaceHolder2_TxtRegno")
        pass_ele = dr.find_element_by_id("ContentPlaceHolder2_TxtPwd")
        submit_ele = dr.find_element_by_id("ContentPlaceHolder2_Submit")
        uname_ele.send_keys(username)
        uname_ele.clear()
        uname_ele.send_keys(username)
        pass_ele.clear()
        pass_ele.send_keys(password)
        submit_ele.click()

    def select_subject(index=0):
        select_ele = dr.find_element_by_id("ContentPlaceHolder2_cboSubject")
        select = webdriver.support.ui.Select(select_ele)
        select.select_by_index(index+1)

    def select_faculty(index=0):
        select_ele = dr.find_element_by_id("ContentPlaceHolder2_cboFaculty")
        select = webdriver.support.ui.Select(select_ele)
        select.select_by_index(index)

    def fill_options(rating='5'):
        big_table = dr.find_elements_by_tag_name("tbody")[6]
        big_list = [(i,i.get_attribute("value")) for i in big_table.find_elements_by_tag_name("input") if len(i.get_attribute("id"))<len("ContentPlaceHolder2_ValidatorCalloutExtender5_Cli")]
        submit_btn = big_list[-1]
        big_list.pop()
        #print(big_list)
        for item, value in big_list:
            if value == rating:
                #print(item)
                item.click()
        submit_btn[0].click()

    def fill_services():
        big_list = [(i,i.get_attribute("value")) for i in dr.find_elements_by_tag_name("input")]
        submit = big_list.pop()
        for item, value in big_list:
            if value=='5':
                try:
                    item.click()
                except Exception as e:
                    print(e)
        if submit[0].get_attribute("id") == 'Submit':
            return False
        submit[0].click()

    def service_login(username=username, password=password):
        dr.find_element_by_id("TxtRegno").send_keys(username)
        dr.find_element_by_id("TxtPwd").send_keys(password)
        dr.find_element_by_id("Submit").click()
    
    try:
        login()
        select_subject()
        while True:
            fill_options()
            print("Filling for {}".format(username))

    except (NoSuchElementException, IndexError) as e:
        print(e)
        dr.close()
        return
        # dr.get(service_url)
        # service_login()
        # not_error = True
        # while not_error:
        #     not_error = fill_services()
        

filename = "Untitled form.csv"
df = pd.read_csv(filename)
args_list = df[[df.columns[-3],df.columns[-2],df.columns[-1]]].values
args_list = [[str(args[0]), str(args[1]), str(args[2])] for args in args_list]

def run_parallel_selenium_processes(datalist, selenium_func):

    pool = Pool()

    # max number of parallel process
    ITERATION_COUNT = cpu_count()-1

    count_per_iteration = len(datalist) / float(ITERATION_COUNT)

    for i in range(0, ITERATION_COUNT):
        list_start = int(count_per_iteration * i)
        list_end = int(count_per_iteration * (i+1))
        pool.apply_async(selenium_func, [datalist[list_start:list_end]])

if __name__=='__main__':
    try:
        with open('save','r') as f:
            count = int(f.read())
    except FileNotFoundError:
        count = 0
    pool = Pool()
    args_list = args_list[count:]
    print(args_list)
    for arg in args_list:
        pool.apply_async(main, arg)
    pool.close()
    pool.join()
    # run_parallel_selenium_processes(args_list, main)


"""
for c in range(count, len(args_list)):
    args = args_list[count]
    main(str(args[0]), str(args[1]), str(args[2]))
    with open('save','w') as f:
        count+=1
        f.write(str(count))
"""



