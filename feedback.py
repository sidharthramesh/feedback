from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def main(username, password, rating=5):
    url = "https://feedback.manipal.edu/sfdfacultyfeedback/login_stud.aspx"
    service_url = "https://feedback.manipal.edu/Services_Feedback/login_mpl.aspx"
    print("[+] For {}".format(username))
    dr = webdriver.Chrome(executable_path="./chromedriver.exe")

    def login(username=username, password=password):
        dr.get(url)
        uname_ele = dr.find_element_by_id("ContentPlaceHolder2_TxtRegno")
        pass_ele = dr.find_element_by_id("ContentPlaceHolder2_TxtPwd")
        submit_ele = dr.find_element_by_id("ContentPlaceHolder2_Submit")
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

roll_no = input("Roll number: ")
password = input("Password: ")
rating = int(input("Rating:(1-5): "))
main(roll_no, password, rating)