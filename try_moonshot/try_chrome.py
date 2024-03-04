import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pywinauto
from pywinauto.keyboard import send_keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_filename(path, filetype):
    name = []
    for root, dirs, files in os.walk(path):
        for i in files:
            if os.path.splitext(i)[1] == filetype:
                name.append(i)
    return name


with open("./file_location.txt", "r", encoding='utf-8') as f:
    path = f.readline()
files = get_filename(path, '.pdf')
nf = len(files)
with open("./prompts.txt", "r", encoding='utf-8') as f:
    prompts = f.readlines()
prompts = [line.strip("\n") for line in prompts]
np = len(prompts)
txt_file = Path('./txt')
txt_file.mkdir(parents=True, exist_ok=True)


driver = webdriver.Chrome()
driver.get('https://kimi.moonshot.cn/')
time.sleep(2)


is_finish_login = (By.CLASS_NAME, 'MuiButtonBase-root')
is_login = EC.visibility_of_element_located(is_finish_login)
is_finish_send = (By.CSS_SELECTOR, 'button[data-testid="msh-chatinput-send-button"]')
is_send = EC.element_to_be_clickable(is_finish_send)
is_finish_output = (By.CSS_SELECTOR, 'button[data-testid="msh-chat-segment-reAnswer"]')
is_output = EC.text_to_be_present_in_element(is_finish_output, text_='再试一次')


# 登录
time.sleep(2)
file_input = driver.find_element(by=By.CSS_SELECTOR, value='label[data-testid="msh-chatinput-upload-button"]')
file_input.click()
WebDriverWait(driver=driver, timeout=600, poll_frequency=0.5, ignored_exceptions=None).until_not(method=is_login)


for index in range(nf):
    file = files[index]
    if index > 0:
        new_page = driver.find_element(by=By.CSS_SELECTOR, value='button[data-testid="msh-header-newchat-btn"]')
        new_page.click()
        time.sleep(5)
        file_input = driver.find_element(by=By.CSS_SELECTOR, value='label[data-testid="msh-chatinput-upload-button"]')

    file_input.click()
    app = pywinauto.Desktop()
    dlg = app["打开"]
    dlg["Toolbar3"].click()
    send_keys(path)
    send_keys("{VK_RETURN}")
    dlg["文件名(&N):Edit"].type_keys(f"{file}", with_spaces=True)
    dlg["打开(&O)"].click()
    WebDriverWait(driver=driver, timeout=600, poll_frequency=0.5, ignored_exceptions=None).until(method=is_send)
    prompt = prompts[0]
    texts = []
    question_input = driver.find_element(by=By.CSS_SELECTOR, value='span[data-slate-node="text"]')
    question_input.send_keys(f'{prompt}')
    send_button = driver.find_element(by=By.CSS_SELECTOR, value='button[data-testid="msh-chatinput-send-button"]')
    send_button.click()
    WebDriverWait(driver=driver, timeout=600, poll_frequency=0.5, ignored_exceptions=None).until(method=is_output)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    get_text = driver.find_element(by=By.XPATH, value=f'//*[@data-index="{2}"]/div/div/div/'
                                                      f'div[@class="container___qPAJp"]/div/div/'
                                                      f'div[@class="markdown___BV5oI"]')
    texts.append(get_text.text)
    for p in range(np-1):
        prompt = prompts[p+1]
        # 输入prompt
        question_input = driver.find_element(by=By.CSS_SELECTOR, value='span[data-slate-node="text"]')
        question_input.send_keys(f'{prompt}')
        time.sleep(1)
        send_button = driver.find_element(by=By.CSS_SELECTOR, value='button[data-testid="msh-chatinput-send-button"]')
        send_button.click()
        time.sleep(4)
        WebDriverWait(driver=driver, timeout=600, poll_frequency=0.5, ignored_exceptions=None).until(method=is_output)
        try:
            down_roll = driver.find_element(by=By.CLASS_NAME, value="css-1i8oban")
            down_roll.click()
        except:
            pass
        get_text = driver.find_element(by=By.XPATH, value=f'//*[@data-index="{(p+2)*2}"]/div/div/div/'
                                                          f'div[@class="container___qPAJp"]/div/div/'
                                                          f'div[@class="markdown___BV5oI"]')
        texts.append(get_text.text)

    WebDriverWait(driver=driver, timeout=600, poll_frequency=0.5, ignored_exceptions=None).until(method=is_output)
    for t in range(np):
        prompt = prompts[t]
        text = texts[t]
        with open(f'./txt/{file.split(".")[0]}.txt', 'a') as f:
            f.write(prompt)
            f.write(':\n')
            f.write(text)
            f.write('\n\n')
