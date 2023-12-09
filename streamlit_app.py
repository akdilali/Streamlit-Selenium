import os
import shutil
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
import requests
import json
from bs4 import BeautifulSoup

@st.cache_resource(show_spinner=False)
def get_logpath():
    return os.path.join(os.getcwd(), 'selenium.log')


@st.cache_resource(show_spinner=False)
def get_chromedriver_path():
    return shutil.which('chromedriver')


@st.cache_resource(show_spinner=False)
def get_webdriver_options():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-features=VizDisplayCompositor")
    return options


def get_webdriver_service(logpath):
    service = Service(
        executable_path=get_chromedriver_path(),
        log_output=logpath,
    )
    return service


def delete_selenium_log(logpath):
    if os.path.exists(logpath):
        os.remove(logpath)


def show_selenium_log(logpath):
    if os.path.exists(logpath):
        with open(logpath) as f:
            content = f.read()
            st.code(body=content, language='log', line_numbers=True)
    else:
        st.warning('No log file found!')


def run_selenium(video_link, logpath):
    name = str()
    with webdriver.Chrome(options=get_webdriver_options(), service=get_webdriver_service(logpath=logpath)) as driver:
        url = "https://www.instagram.com/accounts/login/"
        driver.get(url)
        
        time.sleep(5)  # ensure the page is fully loaded
        
    
        #username_input = driver.find_element_by_css_selector("input[name='username']")
        #password_input = driver.find_element_by_css_selector("input[name='password']")
        username_input = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/div/label/input')
        password_input = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[2]/div/label/input')
    
    
    
        username_input.send_keys("akdilaali")
        password_input.send_keys("aa1trs458112")
    
    
        login_button = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[3]/button")
        login_button.click()
        time.sleep(7)
        # Render the dynamic content to static HTML
        html = driver.page_source
        # print(html)
    
        # Parse the static HTML
        soup = BeautifulSoup(html, "html.parser")
        #divs = soup.find("div", {"class": "flex items-center"})
        #num = int(divs.find("span").text)
        driver.get(video_link)
        time.sleep(5)
        soup = BeautifulSoup(html, "html.parser")
        #print(soup)
        print(soup.find_all("div",class_="_a9zs"))
    
        """
        comment_list = driver.find_elements(By.CLASS_NAME,'_a9zs')
        for i in comment_list:
            print(i.text)
        """
        #/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div[3]/div/div/div[2]/ul/div/li/div/div/div[2]/div[1]/span
        #/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div[3]/div/div/div[4]/ul/div/li/div/div/div[2]/div[1]/span
    
        while True:
            try:
                more_button = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div/ul/div[3]/div/div/li/div/button')
                if more_button:
                    more_button.click()                                       
                    time.sleep(5)
                    print('second_click')
            except:
                break
        comment_list = driver.find_elements(By.CLASS_NAME,'_a9zs')
        for i in comment_list:
            st.write(i.text)


def main():

    st.sidebar.header(':blue[DENEME_sTREMALIT]', divider='blue')

    video_link = st.sidebar.text_input(":blue[INPUT LINK BELOW THE FILED FOR ANALYZE]",placeholder='PASTE LINK')
    #st.sidebar.write(':blue[VIDEO LINK:] ', video_link)
    

    if st.sidebar.button(':blue[START ANALYZE]'):
        st.sidebar.write(':blue[VIDEO LINK:] ', video_link)
        start_time = time.time()
        st.markdown("<h1 style='text-align: center; color: blue;'>YouTube Comment Analysis Dashboard</h1>", unsafe_allow_html=True)
        run_selenium(video_link,logpath)
        st.sidebar.write(":blue[Analysis finished]")
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed Time: {elapsed_time} seconds")
        st.warning('Selenium is running, please wait...')
        #result = run_selenium(logpath=logpath)
        st.info(f'Result -> {result}')
        st.info('Successful finished. Selenium log file is shown below...')
        show_selenium_log(logpath=logpath)



if __name__ == "__main__":
    logpath=get_logpath()
    delete_selenium_log(logpath=logpath)
    st.set_page_config(page_title="Selenium Test", page_icon='✅',
        initial_sidebar_state='collapsed')
    st.title('🔨 Selenium on Streamlit Cloud')
    st.markdown('''This app is only a very simple test for **Selenium** running on **Streamlit Cloud** runtime.<br>
        The suggestion for this demo app came from a post on the Streamlit Community Forum.<br>
        <https://discuss.streamlit.io/t/issue-with-selenium-on-a-streamlit-app/11563><br><br>
        This is just a very very simple example and more a proof of concept.<br>
        A link is called and waited for the existence of a specific class to read a specific property.
        If there is no error message, the action was successful.
        Afterwards the log file of chromium is read and displayed.
        ''', unsafe_allow_html=True)
    st.markdown('---')
    
    st.balloons()
    main()
