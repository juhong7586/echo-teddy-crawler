import pandas as pd
import ssl 
import requests
from bs4 import BeautifulSoup
import pyautogui
import time

def is_valid_url(url):
    if url.startswith('http://') or url.startswith('https://'):
        return True
    return False


def is_valid_num_pages(num_pages):
    try:
        num_pages = int(num_pages)
    except ValueError:
        return False
    
    if num_pages > 0:
        return True
    return False


def get_user_input():
    ## Get the URL from the user
    print('Enter the url of the website you want to crawl:')
    url = input()

    while not is_valid_url(url):
        print('Invalid URL. Please enter a valid URL:')
        url = input()

    ## Get the number of pages to crawl from the user
    print('Enter the number of pages you want to crawl:')
    num_pages = input()
     
    while not is_valid_num_pages(num_pages):
        print('Invalid number of pages. Please enter a valid number of pages:')
        num_pages = input()


    while is_valid_url(url) and is_valid_num_pages(num_pages):

        ## Confirm the user input
        print('Confirm the url and number of pages you want to crawl:')
        print('URL:', url)
        print('Number of pages:', num_pages)

        return(url, num_pages)




def page_crawler(url, QA_data):
    questions = []
    choices_a = []
    choices_b = []
    choices_c = []
    choices_d = []
    answers = []
    
    
    ssl._create_default_https_context = ssl._create_unverified_context
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    results = requests.get(url, headers=header, verify=False)
    soup = BeautifulSoup(results.text, 'html.parser')


    questions_div = soup.find_all('div', class_='card-block')
    
    for container in questions_div:
        question = container.find('div', class_='question_text').p.text
        questions.append(question)

        choice_a = container.find(attrs={"data-choice": "A"}).text
        choices_a.append(choice_a)

        choice_b = container.find(attrs={"data-choice": "B"}).text
        choices_b.append(choice_b)

        choice_c = container.find(attrs={"data-choice": "C"}).text
        choices_c.append(choice_c)

        choice_d = container.find(attrs={"data-choice": "D"}).text
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
    pyautogui.scroll(-10)
    pyautogui.click(2153, 429, button='left')





if __name__ == '__main__':
    print("Loading..")
    ## user_input = get_user_input()

    ## url = user_input[0]
    ## num_pages = user_input[1]

    url = "https://www.itexams.com/exam/BCBA"
    num_pages = 3
    QA_data = pd.DataFrame(columns=['question', 'a', 'b', 'c', 'd', 'answer'])

    page_crawler(url, QA_data)
    print("Done!")
    
