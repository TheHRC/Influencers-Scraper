from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
from creds import username, password


browser = webdriver.Chrome("./driver/chromedriver.exe")
browser.get(f"https://hypeauditor.com/top-instagram") 
# avater = []
# for i in range(1,51):
#     avater.append(tbody.find_elements_by_xpath(f'/html/body/div/div/div/div[1]/div/div[2]/div/div[2]/table/tbody/tr[{i}]/td[3]/div/div[1]/img')[0])


def login(browser, username,password):
    print("from login()")
    signin_btn = browser.find_element_by_css_selector("button[class='btn mt-48 --orange']")
    signin_btn.click()
    time.sleep(1)
    email = browser.find_element_by_name('email')
    email.send_keys(username)

    password_field = browser.find_element_by_name('password')
    password_field.send_keys(password)

    login_btn = browser.find_element_by_css_selector("button[class='button button-big button-block js-btn-loader']")
    login_btn.click()

def get_page(browser, current_page_number):
    if current_page_number != 1:
        browser.get(f"https://hypeauditor.com/top-instagram?p={current_page_number}")
        time.sleep(1.5)
        tbody = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "tbody[class='tbody']")))
        print("TBODY:-> ",tbody)
        return tbody
    else:
        page_list = browser.find_elements_by_xpath("/html/body/div/div/div/div[1]/div/div[2]/div/div[3]/div")[0]

        next_page = page_list.find_element_by_link_text(str(current_page_number+1))
        next_page.click()

        time.sleep(1.5)
        login(browser, username, password)
        print('Login Successful')

    tbody = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "tbody[class='tbody']")))
    return tbody

def write_to_file(usernames, report_pages, followers):
    for un, rp, fl in zip(usernames, report_pages, followers):
        with open("./data/Influencer_data.txt", 'a', encoding="utf-8") as f:
            write_text = f"username:{un}, report_page:{rp}, followers:{fl},\n"
            f.write(write_text)

def get_usernames(browser, page_number):
    tbody = None
    usernames = []
    report_pages = []
    followers = []
   
    print(f"Page:{page_number}")
    print("-"*20)
    tbody = get_page(browser, page_number)
    for i in range(1,51):
        username_data = tbody.find_elements_by_xpath(f"/html/body/div/div/div/div[1]/div/div[2]/div/div[2]/table/tbody/tr[{i}]/td[3]/div/div[2]/a[1]/div[1]/div")
        print("Username:")
        print("*"*30)
        usernames.append(username_data[0].text)
        print(username_data[0].text)
    
        report_pages_data = tbody.find_elements_by_xpath(f"/html/body/div/div/div/div[1]/div/div[2]/div/div[2]/table/tbody/tr[{i}]/td[3]/div/div[2]/a[1]")
        report_pages.append(report_pages_data[0].get_attribute('href'))


        followers_count = tbody.find_elements_by_xpath(f"/html/body/div/div/div/div[1]/div/div[2]/div/div[2]/table/tbody/tr[{i}]/td[5]")
        followers.append(followers_count[0].text)
        print(followers_count[0].text)

    write_to_file(usernames, report_pages, followers)
    return len(usernames)

if __name__ == "__main__":
    total_records = 0
    for page_number in range(1,21):
        records_len = get_usernames(browser,page_number)
        print(f"{records_len} from page {page_number}")
        total_records += records_len
    print(f"Total {total_records} usernames added")