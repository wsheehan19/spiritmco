#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 11:00:07 2021

@author: williamsheehan
"""
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium import webdriver
import json
import time
import datetime
import geckodriver_autoinstaller
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.request
from bs4.element import Comment
import urllib.request
import datetime
import anvil.server
import selenium

print(selenium.__version__)

geckodriver_autoinstaller.install()

profile = webdriver.FirefoxProfile(
    '/Users/williamsheehan/Library/Application Support/Firefox/Profiles/vb9qi9v8.default')

profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.update_preferences()
desired = DesiredCapabilities.FIREFOX

driver = webdriver.Firefox(firefox_profile=profile,
                           desired_capabilities=desired)


#driver.get('https://www.linkedin.com/talent/search?searchContextId=c014905d-5e70-44fb-be23-4b90c97347d4&searchHistoryId=9489926074&searchKeyword=&searchRequestId=fa3f4738-8bbe-492a-bd82-2e8e00479dc5&start=0&uiOrigin=ADVANCED_SEARCH')

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


page_one = 'https://www.linkedin.com/talent/search?searchContextId=c014905d-5e70-44fb-be23-4b90c97347d4&searchHistoryId=9489926074&searchKeyword=&searchRequestId=fa3f4738-8bbe-492a-bd82-2e8e00479dc5&start=0&uiOrigin=ADVANCED_SEARCH'
def recruiter_href(url, pages):
    names = {}
    driver.get(url)
    print('loading...')
    time.sleep(8)
    
    pages_remaining = True
    page_counter = 1
    while pages_remaining:
        print('loading page {} of results'.format(page_counter))
        time.sleep(5)
        body = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        ol = body.find_elements_by_tag_name('ol')[0]
        lis = ol.find_elements_by_tag_name('li')
        for l in lis:
            try:
                a = l.find_element_by_tag_name('a')
                name = a.text
                href = a.get_attribute('href')
                names[name] = href
            except NoSuchElementException:
                continue
        if page_counter == 1:
            xpath = '/html/body/div[2]/div[6]/div/div[2]/div[1]/div[1]/span/section/span/div/form/div[1]/div[2]/span/a'
        else:
            xpath = '/html/body/div[2]/div[6]/div/div[2]/div[1]/div[1]/span/section/span/div/form/div[1]/div[2]/span/a[2]'
        next_page = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.XPATH, xpath)))
        next_page.click()    
        page_counter +=1
        if page_counter > pages:
            pages_remaining = False
            break;
    return names   

dict_less_email = {}

guys = {'Colette Colburn': 'https://www.linkedin.com/talent/profile/AEMAAAD-8ywBl7tsB2Rl2pDI2NrOr2HC1Y_XCmE', 'Cory Vogt, MS': 'https://www.linkedin.com/talent/profile/AEMAAA5OjBUBoaBeKYU4tKV0yc7LIU7KWqdzKj8', 'Amanda Napoles': 'https://www.linkedin.com/talent/profile/AEMAAAeYZU8BWjdcIduhnHzp1ekBDVSeeH2W_0c', 'Louis Bell': 'https://www.linkedin.com/talent/profile/AEMAAAsMG1sBGB3M1Zw6AMfjHkeQnC2-FrZq4LM', 'Tanaisha Brisbon': 'https://www.linkedin.com/talent/profile/AEMAAANn-ooBqGBwXHzEOlBqGFJIOiLW4O1UZGw', 'Kyle Allen': 'https://www.linkedin.com/talent/profile/AEMAAAi0Z8UBLk82H0pv0HPqlWu0nvWM5y-UJmQ',
        'Claudia Soltys, SHRM-CP (She,Her)': 'https://www.linkedin.com/talent/profile/AEMAAAKJNh8BSUgnwr3u9ZBmptVl4zK32NMeUbQ', 'Drew Moorcroft': 'https://www.linkedin.com/talent/profile/AEMAAABcxFMB1gFFQ80l78lrFQiERpRra5_8DsE', 'Julie Angelos': 'https://www.linkedin.com/talent/profile/AEMAAAGNjfUB2IM_zVvW4KlBUlGuKFEhaW-KbX4', 'Akeel Joseph': 'https://www.linkedin.com/talent/profile/AEMAAAJa9x4BMjqad1lZSkv9RLN1GSqlQTsJyRw', 'Venus Brady': 'https://www.linkedin.com/talent/profile/AEMAAAB85uoB95PIl9B-BmyjKwF62AIjoxKZ10I', 'Michael Sweetser': 'https://www.linkedin.com/talent/profile/AEMAAAaGnzcBLlPn-eYyRzItGMoGr3yXe8aysrU', 'Jack Schene': 'https://www.linkedin.com/talent/profile/AEMAAABZNpEBo63_rZIphCYb5jZ8Qj85OW96aZI', 'Etugo Nwokah': 'https://www.linkedin.com/talent/profile/AEMAAACQhPwB1Mri0YlRekx5Jxo5uEMV2kn0U10', 'JAMES H.': 'https://www.linkedin.com/talent/profile/AEMAAAJaLrMBvbCVOLprRzrp98h24aElyyJvqNQ', 'Ruth Greenberg': 'https://www.linkedin.com/talent/profile/AEMAAABJZXUBZTGi78oVnx5maO8ld90o--Zkg7w', 'Kyle Brant': 'https://www.linkedin.com/talent/profile/AEMAAAPIAHUBpyuQ8LZGFmrGbj0ojkB82BH3vBI', 'Allison Backhouse': 'https://www.linkedin.com/talent/profile/AEMAAAEchwsB2QGehHYccomG0FkDUNodxz_xvyg', 'Krushita Shah': 'https://www.linkedin.com/talent/profile/AEMAABzm0XABwsgYQ7C-HG1pRycC6XeBRyod-8M', 'Tara L. Smith': 'https://www.linkedin.com/talent/profile/AEMAAAoN4WcB_yz6rRF2_ARdxEzL9Dw34UgCI8g', 'Daniel Esquibel': 'https://www.linkedin.com/talent/profile/AEMAAADngP4BfQoBL-_AQ3hiprV_LDKmlg7xYbM', 'Alicia Lemmon, PHR': 'https://www.linkedin.com/talent/profile/AEMAAAIVpmMB34CFDTrmLD_5VGJrJyMIM6zq4yI', '💻 Will Nevers': 'https://www.linkedin.com/talent/profile/AEMAAAZK2PQBUxIEhZ2CBFN-L6xUP5moMAF_pdo', 'Melissa Mushlin': 'https://www.linkedin.com/talent/profile/AEMAAABH_5QBCCcLPH54tOrI7hEQbLlL_F0sLlo', 'Josh Cocagne': 'https://www.linkedin.com/talent/profile/AEMAACOc8ogBt8DhjCeq0EhPxjks6Y83R0DtYyU', 'Jim Cunningham': 'https://www.linkedin.com/talent/profile/AEMAAApzM1QBzJ9Yb6RuwXRk3EoLz610RsA0k9c', 'Kenya Howard, MBA': 'https://www.linkedin.com/talent/profile/AEMAAAeK1MoBq86uNV2RHyef_JbfzYr6iiWNcak', 'James Heinlen- MBA': 'https://www.linkedin.com/talent/profile/AEMAAARacMkB7TGkBYvlkDF_hPpKPytKLXXVvlw', 'Pam Emery-Chace': 'https://www.linkedin.com/talent/profile/AEMAAAmZmm8BysxGAqr6qnylqaxMquY1U02Z54I', 'Brad C.': 'https://www.linkedin.com/talent/profile/AEMAAAURsZEBoDuXtfZ_ry68W68avAEZeBhLtks', 'Shannon Davis': 'https://www.linkedin.com/talent/profile/AEMAAAetuzoB5RYtx2rpBbAU8uOnzgP_rPYvJfs', 'David Shelko': 'https://www.linkedin.com/talent/profile/AEMAAAPa0ZEBmgr7-zuzTkkzs2yTK1CpoxeT5hU', 'Jennifer Bruns, MBA, SPHR': 'https://www.linkedin.com/talent/profile/AEMAAAOZ7QABMggC6pDhv7bVFgVeNA2wiiERaQY', 'Pete DeOlympio': 'https://www.linkedin.com/talent/profile/AEMAAAKpEq0BdZyNyCkapTv9pXwunjLD_BGJR_E', 'Julie Manders': 'https://www.linkedin.com/talent/profile/AEMAAAOoqMoBwytudZ40ZrmrRMF2mjnLLZCMIQ0', 'Markeis Coleman, MBA': 'https://www.linkedin.com/talent/profile/AEMAAAmpug4BiZg5W05RklfIMPc99sZFXTipyEI', 'Vikki Carter': 'https://www.linkedin.com/talent/profile/AEMAAADh2N8BPi-nYQ4NNxNBGia5-wBWEV8aWY0', 'Fred Camacho': 'https://www.linkedin.com/talent/profile/AEMAAACzLT4B3__B_LgXI4F5oxeSmMMArPWXBgw', 'Scott Kagan': 'https://www.linkedin.com/talent/profile/AEMAAAE01LUBL2lU4eKhY3kfTvLNlQN0TSLuJKk', 'Lou Steinberg': 'https://www.linkedin.com/talent/profile/AEMAAACkwIgBWyjCC5jDn2ytlWrMtD828pI_4Sw', 'Aleks Flores': 'https://www.linkedin.com/talent/profile/AEMAAAww_pABp3onkA04tPdcSLHhv2iGocII5-w', 'Katherine Lutz, MS': 'https://www.linkedin.com/talent/profile/AEMAAAD1WioBiHTPOH1EtF1MsPS360LkbIvQlao', 'Paul S.': 'https://www.linkedin.com/talent/profile/AEMAAAs7LS4BiowooQwAYSbiTEoAaaMJIUmhBHY', 'Alexis Megeath, PMP, CPHQ': 'https://www.linkedin.com/talent/profile/AEMAAABbUo4BDFiLd0ERJDJ1SaM-IGb4FP357Rs', 'Terrance Logan': 'https://www.linkedin.com/talent/profile/AEMAAAoIkkEBKmr8umGNizk-4wXlAdN52FimMvs', 'Mary Francis McLaughlin, Ph.D.': 'https://www.linkedin.com/talent/profile/AEMAAAoudQAB5R9zGvxMK54n4k4qZ7Ym7RCStco', 'Sean Campbell, MBA': 'https://www.linkedin.com/talent/profile/AEMAAACbCngBaKhp8MNKijAjBTYDPIjdOSSjANs', 'Arynn E.': 'https://www.linkedin.com/talent/profile/AEMAAAIu4OgBA35gg22-8VsJEVnl_LJgQ9rN5MM', 'JP Brown, CPA': 'https://www.linkedin.com/talent/profile/AEMAAAF6WJQByvl8AMYP4iEuXtucdBe0f4ewh0s', 'Yemisi Adetunji, MBA': 'https://www.linkedin.com/talent/profile/AEMAAAVVARABYytvOkaR94_d3SWsG7Yo1QUPdao', 'Andrew Pashman': 'https://www.linkedin.com/talent/profile/AEMAAABytesBwJZqasLxkV2grr_xM9QTEpeXf18', 'Nicholas R.': 'https://www.linkedin.com/talent/profile/AEMAAAShQbQBef8RQQDknjOkpZK81jlCdN1BmLg', 'Jasmin Johansen-Hickman': 'https://www.linkedin.com/talent/profile/AEMAAAbom7cBW9GRGCGHMWWkAcRVrnxNBbDJ1a4', 'Steven Fuhrman': 'https://www.linkedin.com/talent/profile/AEMAAAj1cQcB6zEOfmBkvN2c-cemdPuMvPWJ9Ss', 'Dee Marsden': 'https://www.linkedin.com/talent/profile/AEMAAA8tEvoBcP1kUsj73B_lq5SHUKegfdM-asA', 'Jake Konoske': 'https://www.linkedin.com/talent/profile/AEMAAApqUf4B67u1hjy0kM5cw1qLz8mBfD35qbg', 'Jacqueline (Jackie) Weder': 'https://www.linkedin.com/talent/profile/AEMAAAGJFYkBz5eBybulMGlbKuLh2d3kX1CQKvs', 'Brian Locke': 'https://www.linkedin.com/talent/profile/AEMAAAAo9mEB1EVHyeiOB1O8txcbq-Za452RdWM', 'Dana Barrett, MBA, SHRM-CP': 'https://www.linkedin.com/talent/profile/AEMAAAf7O8UBrtwP1_uTxqZ5iZXTXepG-WaOR54', 'Mario L.': 'https://www.linkedin.com/talent/profile/AEMAAAJOn3MB8LTZnMV38TM7fZX-DsMQYL2pr5E', 'Deborah Collins': 'https://www.linkedin.com/talent/profile/AEMAAAENb5sBVOrXxPq_9J9zifsDD5fs6Yidqnc', 'Ryan Korchinski': 'https://www.linkedin.com/talent/profile/AEMAAAJGa_UBrMz2xS9rZVbwnnxjUaBM6OY9zNw', 'Kristine Phisayavong': 'https://www.linkedin.com/talent/profile/AEMAAAzU8zwBFgvBn5z3katqs5bJ02A88ZwWc3s', 'Paula Robison': 'https://www.linkedin.com/talent/profile/AEMAAAC7puwBlzduCCM0HB-0dqa6RTgCBrQsTwc', 'Alex Harwitz': 'https://www.linkedin.com/talent/profile/AEMAAAAbd6wBUvtbFP5fdbytnBTUhy4FWYQ5mzg', 'Mary Leamy': 'https://www.linkedin.com/talent/profile/AEMAAAaM--8B-B2URuysEv6XGsiGD8bU62-suog', 'Greg Rideout': 'https://www.linkedin.com/talent/profile/AEMAAAPZxUIBR1gxLVndjHJGrKNwtZX1hCoT3vc', 'Stephanie Valenzuela': 'https://www.linkedin.com/talent/profile/AEMAAAleXhgBKYX0NLu3Lw5UdnwAX_sFBYZdeo0', 'Chad Bittner': 'https://www.linkedin.com/talent/profile/AEMAAADIGYkBN2AMKprxBaC4BleMElu5wNTPuQo', 'LaTresse Snead': 'https://www.linkedin.com/talent/profile/AEMAAAJGv3EB9P-ZYFAChk_e11mhHzAkg907jYM', 'Patrick Ma': 'https://www.linkedin.com/talent/profile/AEMAAAG4IzwBjv0tM_sDYq4a-uzRcdGrUQ87HNM', 'Tracie Martin, MBA': 'https://www.linkedin.com/talent/profile/AEMAAAcVT5MBLaueIuNLRYhy1B4KUCC2oW6Nb3A', 'Allison Swearingen': 'https://www.linkedin.com/talent/profile/AEMAACO39PYBNl4sEBEcrdnLiCnQ5NRju3A2MM0', 'Amy Severino': 'https://www.linkedin.com/talent/profile/AEMAAACs9pMBaDBxl9CcKQh2oiuu3IqUiavObYQ', 'Ryan Peterson': 'https://www.linkedin.com/talent/profile/AEMAAAEUEYoBf1WNc3iKDZ5HpQqD4B2NFV-bPj4'}
  
def recruiter_info(person, link):
    person = person.split(', ')[0]
    person = person.split('- ')[0]
    driver.get(link)
    print("loading {}'s profile".format(person))
    button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[6]/div/div[2]/main/div/span/div/div/header/section/div[1]/div[1]/div[2]/span/button')))
    button.click()
    xp = '/html/body/div[2]/aside[2]/div[1]/div[1]/div/a'
    a = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xp)))
    public_profile = a.get_attribute('href')
    
    try:
        xp = '/html/body/div[2]/div[6]/div/div[2]/main/div/span/div/div/header/section/div[1]/div[1]/section/div/div[2]/div[2]/div'
        loc = driver.find_element_by_xpath(xp).text
    except NoSuchElementException:
        xp = '/html/body/div[2]/div[6]/div/div[2]/main/div/span/div/div/header/section/div[1]/div[1]/section/div/div[2]/div[3]/div'
        loc = driver.find_element_by_xpath(xp).text
        
    
    background_card = driver.find_element_by_xpath('/html/body/div[2]/div[6]/div/div[2]/main/div/span/div/div/div[2]/div/section[2]')
    jobs = background_card.find_elements_by_tag_name('div')[0].find_elements_by_tag_name('li')
    current = jobs[0]
    dds = current.find_elements_by_tag_name('dd')
    position = dds[0].find_element_by_tag_name('a').text
    try:
        company = dds[1].find_element_by_tag_name('a').text.split(' •')[0]
    except NoSuchElementException:
        try:
            company = current.find_element_by_tag_name('strong').text.split(' •')[0]
        except NoSuchElementException:
             company = dds[1].text.split(' •')[0]
        
    try: 
        duration = dds[2].find_element_by_tag_name('span').text
    except NoSuchElementException:
        duration = dds[1].find_element_by_tag_name('span').text
    
    school = ''
    degree = ''
    years = ''
    field_of_study = ''
    job_divs = background_card.find_elements_by_tag_name('div')[0].find_elements_by_tag_name('div')
    try:
        edu = background_card.find_elements_by_tag_name('div')[len(job_divs) + 1].find_elements_by_tag_name('li')
        recent = edu[0]
        ddss = recent.find_elements_by_tag_name('dd')
        school = ddss[0].text
        for d in ddss:
            if ' – ' in d.text:
                years = d.text
                
            if 'Degree name' in d.text:
                degree = d.text.split('Degree name\n')[-1]
                if 'Field of study' in degree:
                    degree = degree.split('Field of study')[0].split(' •')[0]
        
            if 'Field of study' in d.text:
                field_of_study = d.text.split('Field of study\n')[-1].split(' •')[0]
    except IndexError:
        pass
    
    dict_less_email[person] = {'Location': loc, 'Current Position': position, 'Current Company': company,
                               'Employment Dates': duration, 'Most Recent Education': school, 'Years Attended': years,
                               'Degree': degree,'Field of Study': field_of_study, 'Public Profile': public_profile}
   
def apollo_href(name, company, location):
    """
    

    Parameters
    ----------
    name : name of person
    company : company of employment, as listed on person's LinkedIn Profile

    Returns
    -------
    None.

    """
    url = 'https://app.apollo.io/#/companies?prospectedByCurrentTeam[]=no&finderViewId=5a205be19a57e40c095e1d5f&page=1'
    driver.get(url)
    driver.maximize_window()
    if check_exists_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/form/div[1]/div') == True:
        print('gotta log in')
        google_login = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#provider-mounter > div > div.zp_2Pnik > div.zp_2YB95 > div > div.zp_1QN2s > div > div.zp_p7Ra4.zp_2ZLGm > div > form > div:nth-child(1) > div")))
        google_login.click()
        try:
            email = driver.find_element_by_id("identifierId")
            email.send_keys('wsheehan.spiritmco@gmail.com')
            next_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#identifierNext > div > button > span")))
            next_button.click()
            bypass = False
        except NoSuchElementException:
            auto_login = True
            bypass = False
            print('auto login')
    
        if bypass == True:
            ppl_css = 'a.zp_2EIcj:nth-child(1)'
            people = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ppl_css)))
            people.click()
        if auto_login == True:
            search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sidebar-nav-prospect-search")))
            search.click()
            ppl_css = 'a.zp_2EIcj:nth-child(1)'
            people = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ppl_css)))
            people.click()
    else:
        search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sidebar-nav-prospect-search")))
        search.click()
        ppl_css = 'a.zp_2EIcj:nth-child(1)'
        people = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ppl_css)))
        people.click()
    #lvl = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div[2]')
    main = driver.find_element_by_tag_name('body')
    lvl = main.find_element_by_id('provider-mounter').find_element_by_tag_name('div').find_element_by_css_selector('.zp_4kNyT > div:nth-child(2) > div:nth-child(2)').find_element_by_tag_name('div').find_elements_by_tag_name('div')[0].find_element_by_css_selector('.zp_3cHPT')
    lvl2 = lvl.find_element_by_css_selector('.zp_3Lzj1')
    lvl3 = lvl2.find_element_by_css_selector('.zp_3Lzj1 > div:nth-child(1)')
    lvl4 = lvl3.find_element_by_css_selector('.zp_p7Ra4')
    lvl5 = lvl4.find_element_by_css_selector('.zp_iChR6')
    lvl6 = lvl5.find_element_by_css_selector('.finder-explorer-sidebar-shown')
    lvl7 = lvl6.find_element_by_css_selector('.zp_2OPXS')
    lvl8 = lvl7.find_element_by_css_selector('.zp_70GAc')
    lvl9 = lvl8.find_element_by_css_selector('.zp_2rDPH')
    lvl10 = lvl9.find_element_by_css_selector('.zp_2dK1W')
    lvl11 = lvl10.find_element_by_css_selector('.zp-field')
    lvl12 = lvl11.find_element_by_css_selector('.input-container')
    lvl13 = lvl12.find_element_by_css_selector('.zp_25N3i')
    
    
    search = lvl13.find_element_by_tag_name('input')
    search.clear()
    search.send_keys(name, ' ', company, '\ue007')
    
    #person = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div/div/div/div/div[2]/div/table/tbody/tr')
    try:
        print('searching "{name} {company}"'.format(name=name, company=company))
        person = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div/div/div/div/div[2]/div/table/tbody/tr')))
        href = person.find_element_by_class_name('zp_yJfMM').find_element_by_class_name('zp_1sGdg').find_element_by_class_name('zp_EqOJn').find_element_by_class_name('zp_PrhFA').find_element_by_tag_name('a').get_attribute('href')
    except TimeoutException:
        search.clear()
        search.send_keys(name, ' ', location, '\ue007')
        print('searching "{name} {location}"'.format(name=name, location=location))
        try:
            person = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div/div/div/div/div[2]/div/table/tbody/tr')))
            href = person.find_element_by_class_name('zp_yJfMM').find_element_by_class_name('zp_1sGdg').find_element_by_class_name('zp_EqOJn').find_element_by_class_name('zp_PrhFA').find_element_by_tag_name('a').get_attribute('href')
        except:
            search.clear()
            search.send_keys(name, '\ue007')
            print('searching "{name}"'.format(name=name))
            try:
                person = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div/div/div/div/div[2]/div/table/tbody/tr')))
                href = person.find_element_by_class_name('zp_yJfMM').find_element_by_class_name('zp_1sGdg').find_element_by_class_name('zp_EqOJn').find_element_by_class_name('zp_PrhFA').find_element_by_tag_name('a').get_attribute('href')
            except:
                print('{name} not in Apollo database'.format(name=name))
                href = ''
    except StaleElementReferenceException:
        search.clear()
        search.send_keys(name, ' ', location, '\ue007')
        print('searching "{name} {location}"'.format(name=name, location=location))
        try:
            person = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div/div/div/div/div[2]/div/table/tbody/tr')))
            href = person.find_element_by_class_name('zp_yJfMM').find_element_by_class_name('zp_1sGdg').find_element_by_class_name('zp_EqOJn').find_element_by_class_name('zp_PrhFA').find_element_by_tag_name('a').get_attribute('href')
        except:
            search.clear()
            search.send_keys(name, '\ue007')
            print('searching "{name}"'.format(name=name))
            try:
                person = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div/div/div/div/div[2]/div/table/tbody/tr')))
                href = person.find_element_by_class_name('zp_yJfMM').find_element_by_class_name('zp_1sGdg').find_element_by_class_name('zp_EqOJn').find_element_by_class_name('zp_PrhFA').find_element_by_tag_name('a').get_attribute('href')
            except:
                print('{name} not in Apollo database'.format(name=name))
                href = ''
    
    return href


def apollo_sign_in():
    try:
        google_login = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#provider-mounter > div > div.zp_2Pnik > div.zp_2YB95 > div > div.zp_1QN2s > div > div.zp_p7Ra4.zp_2ZLGm > div > form > div:nth-child(1) > div")))
        google_login.click()
        try:
            email = driver.find_element_by_id("identifierId")
            email.send_keys('wsheehan.spiritmco@gmail.com')
            next_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#identifierNext > div > button > span")))
            next_button.click()
            bypass = False
        except NoSuchElementException:
            auto_login = True
            bypass = False
            print('auto login')
    except TimeoutException:
        print('logged in')
        bypass = True
        auto_login = False
    
    if bypass == True:
        ppl_css = 'a.zp_2EIcj:nth-child(1)'
        people = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ppl_css)))
        people.click()
    if auto_login == True:
        search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sidebar-nav-prospect-search")))
        search.click()
        ppl_css = 'a.zp_2EIcj:nth-child(1)'
        people = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ppl_css)))
        people.click()

def get_email(link):
    """
    

    Parameters
    ----------
    link : link to person's Apollo.io page

    Returns
    -------
    email

    """
    driver.get(link)
    driver.maximize_window()
    if check_exists_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/form/div[1]/div') == True:
        print('gotta log in')
        google_login = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#provider-mounter > div > div.zp_2Pnik > div.zp_2YB95 > div > div.zp_1QN2s > div > div.zp_p7Ra4.zp_2ZLGm > div > form > div:nth-child(1) > div")))
        google_login.click()
        try:
            email = driver.find_element_by_id("identifierId")
            email.send_keys('wsheehan.spiritmco@gmail.com')
            next_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#identifierNext > div > button > span")))
            next_button.click()
        except NoSuchElementException:
            print('auto login')
        
        driver.get(link)
    
    try:
        access = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.zp-button:nth-child(2) > div:nth-child(2)")))
        access.click()
        time.sleep(2)
        email = driver.find_element_by_css_selector('.zp_3v1d1').text
        print(email)
    except ElementNotInteractableException:
        print('no email on page')
        email = ''
    
    
    return email        


start = datetime.datetime.now()
names = recruiter_href(page_one, 4)
print(len(names))

for n in names:
    try:
        recruiter_info(n, names[n])
    except Exception as e:
        print(e)
        time.sleep(45)
        continue

for human in dict_less_email:
    data = dict_less_email[human]
    company = data['Current Company']
    location = data['Location']
    try:
        link = apollo_href(human, company, location)
        #dict_less_email[human]['Apollo Link'] = link
    except TimeoutException:
        link = ''
        #dict_less_email[human]['Apollo Link'] = ''
        print('{name} not in apollo database'.format(name=human))
    except ElementClickInterceptedException:
        driver.close()
        driver = webdriver.Firefox(firefox_profile=profile,
                            desired_capabilities=desired)
        try:
            link = apollo_href(human, company, location)
            #dict_less_email[human]['Apollo Link'] = link
        except TimeoutException:
            link = ''
            #dict_less_email[human]['Apollo Link'] = ''
            print('{name} not in apollo database'.format(name=human))
        except Exception as e:
            link = ''
            print(e)
            print('double error searching for ' + human)
            #dict_less_email[human]['Apollo Link'] = ''
        continue
    print(human, link)
    dict_less_email[human]['Apollo Link'] = link
    

out_dict = {}
for human in dict_less_email:
    print('pulling email for ' + human)
    data = dict_less_email[human]
    apollo_link = data['Apollo Link']
    if len(apollo_link) >2:
        try:
            email = get_email(apollo_link)
        except Exception as e:
            print(e)
            print('error pulling email for ' + human)
            email = ''
    else:
        email = ''
        print(human + ' not in apollo, so cant grab email')
    data['Email'] = email
    out_dict[human] = data
    
dataframe = pd.DataFrame(out_dict).T
dataframe.to_csv('recruit2.csv')   
end = datetime.datetime.now()

print(start)
print(end)
print(end-start)
    
    
    
    