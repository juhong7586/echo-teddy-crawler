import pandas as pd
import ssl 
import requests
from bs4 import BeautifulSoup
import time
import selenium.common
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



extension_folder_path = "/Users/juhong/Library/Application Support/Google/Chrome/Default/Extensions"
extension_path = extension_folder_path + "/mpbjkejclgfgadiemmefgebjfooflfhl"
packed_extension_path = extension_path + "/3.1.0_0.crx"

url = "https://www.itexams.com/exam/BCBA"

QA_data = pd.DataFrame(columns=['question', 'a', 'b', 'c', 'd', 'answer'])

chrome_options = webdriver.ChromeOptions()
chrome_options.add_extension(packed_extension_path)
chrome_options.add_argument("window-size=1024,600")

driver = webdriver.Chrome(options=chrome_options)
actions = ActionChains(driver)


def is_valid_num_pages(num_pages):
    try:
        num_pages = int(num_pages)
        return num_pages > 0
    except ValueError:
        return False


def get_user_input():
    print('Enter the number of pages you want to crawl:')
    num_pages = input()
     
    while not is_valid_num_pages(num_pages):
        print('Invalid number of pages. Please enter a valid number of pages:')
        num_pages = input()

    return(num_pages)


def page_crawler(html, QA_data):
    questions, choices_a, choices_b, choices_c, choices_d, answers = [], [], [], [], [], []

    soup = BeautifulSoup(html, 'html.parser')

    questions_div = soup.find_all('div', class_='card-block')
    
    for container in questions_div:
        question = ' '.join(container.find('div', class_='question_text').p.text.split())
        questions.append(question)

        choice_a = ' '.join(container.find(attrs={"data-choice": "A"}).text.split())
        choices_a.append(choice_a)

        choice_b = ' '.join(container.find(attrs={"data-choice": "B"}).text.split())
        choices_b.append(choice_b)

        choice_c = ' '.join(container.find(attrs={"data-choice": "C"}).text.split())
        choices_c.append(choice_c)

        choice_d = ' '.join(container.find(attrs={"data-choice": "D"}).text.split())
        choices_d.append(choice_d)

        answer_container = container.find("div", class_="answer_block green accent-1")
        answer = answer_container["data-answer"]
        answers.append(answer)

    QA_dict_page = {'question' : questions, 'a' : choices_a, 'b' : choices_b, 'c' : choices_c, 'd' : choices_d, 'answer' : answers}
    QA_data_page = pd.DataFrame(QA_dict_page)
    QA_data = pd.concat([QA_data, QA_data_page], ignore_index=True)
    print(QA_data)
    return QA_data

def move_around():
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "open-captcha"))
    ).click()
    print("Next page clicked")
    

    timeout_seconds = 30
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        try:
            ## from: https://aeng-is-young.tistory.com/entry/Google-reCAPTCHA-selenium%EC%9C%BC%EB%A1%9C-%EB%AC%B4%EB%A0%A5%ED%99%94-%EC%8B%9C%EC%BC%9C%EB%B3%B4%EA%B8%B0
            WebDriverWait(driver, 10).until((EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@title='reCAPTCHA']"))))
            WebDriverWait(driver, 10).until((EC.element_to_be_clickable((By.XPATH,"//*[@id='recaptcha-anchor']/div[1]")))).click()

            driver.switch_to.default_content()

            WebDriverWait(driver,10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@title='recaptcha challenge expires in two minutes']")))

            time.sleep(3)
            break

        except selenium.common.exceptions.StaleElementReferenceException:
            print(f"Retrying reCAPTCHA...")
            driver.switch_to.default_content()
            time.sleep(2)
        except Exception as e:
            print(f"Error: {e}")
            break   

    while True: 
        try:
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='button-holder help-button-holder']"))).click()
        
        except selenium.common.exceptions.StaleElementReferenceException:
            print("Retrying help button click...")
            pass
        except selenium.common.exceptions.ElementClickInterceptedException:
            print("Bypassed.")
            break
        except Exception as e:
            print(f"Error clicking help button: {e}")
            break
            

if __name__ == "__main__":
    print("Loading..")
    num_pages = get_user_input()

    driver.get(url)
    time.sleep(3)

    for i in range(int(num_pages)):
        QA_data = page_crawler(driver.page_source, QA_data)
        move_around()

    print(QA_data)
    driver.quit()
    print("Done!")


