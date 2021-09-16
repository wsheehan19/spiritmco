#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 12:39:53 2021

@author: williamsheehan
"""
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
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


geckodriver_autoinstaller.install()

profile = webdriver.FirefoxProfile(
    '/Users/williamsheehan/Library/Application Support/Firefox/Profiles/vb9qi9v8.default')

profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.update_preferences()
desired = DesiredCapabilities.FIREFOX

driver = webdriver.Firefox(firefox_profile=profile,
                           desired_capabilities=desired)
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def search(keywords=None, 
           # custom_lists=None, past_activity=None, 
           geography=None, relationship=None, company=None,
           industry=None, headcount=None, seniority=None, function=None, 
           title=None, pages=10):
    """
    searches LinkedIn Sales navigator with given filters
    Parameters:
        keywords: Boolean search string, default None
        geography: list of locations, default None
        relationship: list, default None
            possible list elements: 1st, 2nd, group, 3rd+
        company: list of companies, default None
        industry: list of industries, default None
        headcount: [min, max], default None
        seniority: list, default None
            possible list values: Owner, Partner, CXO, VP, Director, Manager, Senior, Entry, Training, Unpaid
        function: string or list, default None
        title: string or list, default None
    
    Returns:
        list of urls of pages of results that fit the given parameters
    
    """
    url = 'https://www.linkedin.com/sales/search/people'
    driver.get(url)
    driver.maximize_window()
    time.sleep(3)
    if keywords:
        search = driver.find_element_by_class_name('search-filter__form').find_element_by_css_selector('.search-filter-keywords').find_element_by_tag_name('div').find_element_by_class_name('flex').find_element_by_tag_name('div').find_element_by_class_name('ember-view').find_element_by_tag_name('div').find_element_by_tag_name('input')
        search.send_keys(keywords)
        
    filters = driver.find_elements_by_tag_name('li')
    geo = filters[8]
    rel = filters[9]
    co = filters[10]
    ind = filters[11]
    count = filters[12]
    sen = filters[13]
    func = filters[14]
    t = filters[15]
    
    if geography:
        a = geo.find_element_by_tag_name('div')
        a.click()
        search = a.find_element_by_tag_name('div').find_elements_by_tag_name('div')[4]
        for place in geography:
            search.find_element_by_tag_name('input').send_keys(place)
            result = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.button--unstyled:nth-child(1)')))
            result.click()
    
    if relationship:
        a = rel.find_element_by_tag_name('div')
        a.click()
        if ('1st' in relationship) and ('2nd' in relationship) and ('group' in relationship) and ('3rd+' in relationship):
            first = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(1)')))
            first.click()
            second = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(1)')))
            second.click()
            group = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(1)')))
            group.click()
            third = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(1)')))
            third.click()
        if ('1st' in relationship) and ('2nd' in relationship) and ('group' in relationship) and ('3rd+' not in relationship):
            first = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(1)')))
            first.click()
            second = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(1)')))
            second.click()
            group = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(1)')))
            group.click()     
        if ('1st' in relationship) and ('2nd' in relationship) and ('group' not in relationship) and ('3rd+' in relationship):
            first = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(1)')))
            first.click()
            second = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(1)')))
            second.click()
            third = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(2)')))
            third.click()
        if ('1st' in relationship) and ('2nd' not in relationship) and ('group' in relationship) and ('3rd+' in relationship):
            first = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(1)')))
            first.click()
            group = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(2)')))
            group.click()
            third = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(2)')))
            third.click()
        if ('1st' not in relationship) and ('2nd' in relationship) and ('group' in relationship) and ('3rd+' in relationship):
            second = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(2)')))
            second.click()
            group = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(2)')))
            group.click()
            third = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(2)')))
            third.click()        
        if ('1st' in relationship) and ('2nd' in relationship)and ('group' not in relationship) and ('3rd+' not in relationship):    
            first = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(1)')))
            first.click()
            second = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(1)')))
            second.click()  
        if ('1st' in relationship) and ('2nd' not in relationship)and ('group' in relationship) and ('3rd+' not in relationship):
            first = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(1)')))
            first.click()
            group = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(2)')))
            group.click()
        if ('1st' in relationship) and ('2nd' not in relationship)and ('group' not in relationship) and ('3rd+' in relationship):
            first = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(1)')))
            first.click()
            third = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(3)')))
            third.click()
        if ('1st' not in relationship) and ('2nd' in relationship)and ('group' in relationship) and ('3rd+' not in relationship):
            second = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(2)')))
            second.click()
            group = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(2)')))
            group.click()
        if ('1st' not in relationship) and ('2nd' in relationship)and ('group' not in relationship) and ('3rd+' in relationship):
            second = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(2)')))
            second.click()
            third = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(3)')))
            third.click()
        if ('1st' not in relationship) and ('2nd' not in relationship)and ('group' in relationship) and ('3rd+' in relationship):
            group = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(3)')))
            group.click()
            third = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(3)')))
            third.click()
        if ('1st' in relationship) and ('2nd' not in relationship)and ('group' not in relationship) and ('3rd+' not in relationship):
            first = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(1)')))
            first.click()
        if ('1st' not in relationship) and ('2nd' in relationship)and ('group' not in relationship) and ('3rd+' not in relationship):
            second = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(2)')))
            second.click()
        if ('1st' not in relationship) and ('2nd' not in relationship)and ('group' in relationship) and ('3rd+' not in relationship):  
            group = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(3)')))
            group.click()
        if ('1st' not in relationship) and ('2nd' not in relationship)and ('group' not in relationship) and ('3rd+' in relationship):
            third = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(4)')))
            third.click()
    
    if company:
        a = co.find_element_by_tag_name('div')
        a.click()
        search = a.find_element_by_tag_name('div').find_elements_by_tag_name('div')[4]
        for c in company:
            search.find_element_by_tag_name('input').send_keys(c)
            result = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(1) > button:nth-child(2)')))
            result.click()
            
    if industry:
        a = ind.find_element_by_tag_name('div')
        a.click()
        search = a.find_element_by_tag_name('div').find_elements_by_tag_name('div')[4]
        for i in industry:
            search.find_element_by_tag_name('input').send_keys(i)
            # result = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.button--unstyled:nth-child(1)')))
            result = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.button--unstyled:nth-child(1)')))
            # WebDriverWait.until(EC.invisibility_of_element_located((By.CLASS_NAME,
            #   "eah-product-lockup__text")))
            driver.execute_script("arguments[0].click();", result)
            # result.click()
            
    if headcount:
        min = headcount[0]
        max = headcount[-1]
        a = count.find_element_by_tag_name('div')
        a.click()
        try:
            if max == None:
                if min < 10:
                    for _ in range(9):
                        options = a.find_elements_by_tag_name('li')
                        options[-1].find_element_by_tag_name('button').click()
                if (min > 10) and (min <= 50):
                    for _ in range(7):
                        options = a.find_elements_by_tag_name('li')
                        options[-1].find_element_by_tag_name('button').click()
                if (min > 50) and (min <= 200):
                    for _ in range(6):
                        options = a.find_elements_by_tag_name('li')
                        options[-1].find_element_by_tag_name('button').click()       
                if (min > 200) and (min <= 500):
                    for _ in range(5):
                        options = a.find_elements_by_tag_name('li')
                        options[-1].find_element_by_tag_name('button').click()
                if (min > 500) and (min <= 1000):
                    for _ in range(4):
                        options = a.find_elements_by_tag_name('li')
                        options[-1].find_element_by_tag_name('button').click()
                if (min > 1000) and (min <= 5000):
                    for _ in range(3):
                        options = a.find_elements_by_tag_name('li')
                        options[-1].find_element_by_tag_name('button').click()
                if (min > 5000) and (min <= 10000):
                    for _ in range(2):
                        options = a.find_elements_by_tag_name('li')
                        options[-1].find_element_by_tag_name('button').click()
                if (min >= 10000):
                    options = a.find_elements_by_tag_name('li')
                    options[-1].find_element_by_tag_name('button').click()
        except StaleElementReferenceException:
            print('stale')
                
    if seniority:
        a = sen.find_element_by_tag_name('div')
        a.click()
        for s in seniority:
            options = a.find_elements_by_tag_name('li')
            for o in options:
                pos = o.find_element_by_tag_name('button')
                if pos.text == s:
                    pos.click()
                    break
        
    if function:
        a = func.find_element_by_tag_name('div')
        a.click()
        search = a.find_element_by_tag_name('div').find_elements_by_tag_name('div')[4]
        for f in function:
            search.find_element_by_tag_name('input').send_keys(f)
            result = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.button--unstyled:nth-child(1)')))
            result.click()
            
    if title:
        a = t.find_element_by_tag_name('div')
        a.click()
        search = a.find_element_by_tag_name('div').find_elements_by_tag_name('div')[4]
        for t in title:
            search.find_element_by_tag_name('input').send_keys(t)
            result = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.t-sans:nth-child(1) > button:nth-child(1)')))
            result.click()
    urls = []
    a = driver.current_url
    query_str = a.split('page=')[0] + 'page={}' + a.split('page=')[-1][1:]
    for n in range(1, pages):
        s = query_str.format(n)
        urls.append(s)
    
    print(urls)
    return urls

names = {}
def LI_href(url):
    """
    

    Parameters
    ----------
    url : url of 1 page of search results on LI Sales Navigator

    Returns
    -------
    None.

    """
    profile = webdriver.FirefoxProfile(
    '/Users/williamsheehan/Library/Application Support/Firefox/Profiles/vb9qi9v8.default')

    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference('useAutomationExtension', False)
    profile.update_preferences()
    desired = DesiredCapabilities.FIREFOX
    
    driver = webdriver.Firefox(firefox_profile=profile,
                               desired_capabilities=desired)
    driver.get(url)
    body = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'main')))
    elements = body.find_elements_by_tag_name('li')
    for e in elements[20:59]:
        text = e.text
        if 'Select' in text:
            som = e.get_attribute('data-scroll-into-view')
            if som is not None:
                href = 'https://www.linkedin.com/sales/people/{}?_ntb=GXKlwyT6R9esbDlnDcsjRA%3D%3D'.format(som.split('le:(')[-1][:-1])
            if som is None: 
                href = ''
            if 'Profile result' in text:
                name = text.split('Select ')[-1].split('\nProfile result ')[0]
                if ',' in name:
                    name = name.split(',')[0]
                names[name] = {'name': name, 'href': href}
            if 'Profile result' not in text:
                if ',' in text:
                    name = text.split('Select ')[-1].split(',')[0]
                    names[name] = {'name': name, 'href': href}
                if '(' in text:
                    name = text.split('Select ')[-1].split(' (')[0]
                    names[name] = {'name': name, 'href': href}
                if (',' not in text) and ('(' not in text):
                    name = text.split('Select ')[-1]
                    names[name] = {'name': name, 'href': href}
    
    driver.close()
    return None             


LI_info_dict = {}

# @retry(stop_max_attempt_number=7)
def LI_info(person, lnk):
    """
    

    Parameters
    ----------
    person : name of person
    lnk : link to person's LinkedIn profile

    Returns
    -------
    None.

    """
    driver.get(lnk)
    try:
        show_more_exp = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/div[1]/div/div[1]/section[1]/div/button/span')))
        show_more_exp.click()
    except TimeoutException:
        print('no more past experience to show')
    try:
        ex = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/div[1]/div/div[1]/section[1]/div/ul')))
        exp = ex.find_elements_by_tag_name('li')
        past_experience = {}
        for e in exp:
            whole = e.text
            position = whole.split('\nCompany Name')[0]
            company = whole.split('Company Name')[-1].split('\nDates Employed')[0][1:]
            duration = whole.split('Employment Duration')[-1][1:].split('mo')[0] + 'mos'
            if 'Description' in duration:
                duration = duration.split('\nDescription')[0]
            if 'Location' in whole:
                location = whole.split('Location')[-1][1:]
                if 'Description' in location:
                    location = location.split('\nDescription')[0]
                else:
                    pass
            else:
                location = ''                
            if 'Description' in whole:        
                description = whole.split('Description')[-1]
                if 'Media' in description:
                    description = description.split('Media')[0]
                else:
                    pass
            else:
                description = ''
             
            if company not in position:
            #if ('.png' not in company) or ('.jpg' not in company) or (position != location):
                past_experience.update({company:{'Company': company, 'Position': position,'Location': location, 'Duration': duration, 'Description': description}})
    except TimeoutException:
        print('no experience on profile')
    
    try:
        show_more_ed = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember118"]')))
        show_more_ed.click()
    except:
        print('no more education to show')
    
    education = {}
    try:
        ed = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/div[1]/div/div[1]/section[2]/div/ul')))
        educ = ed.find_elements_by_tag_name('li')
        for e in educ:
            time.sleep(2)
            whole = e.text
            school = whole.split('\nDegree Name')[0]
            if 'Field Of Study' in whole:
                degree_name = whole.split('Degree Name')[-1].split('\nField Of Study')[0][1:]
                field_of_study = whole.split('Field Of Study')[-1][1:].split('\nDates attended')[0]
            else:
                degree_name = whole.split('Degree Name')[-1].split('\nDates attended')[0][1:]
                field_of_study = ''
            dates = whole.split('expected graduation')[-1][1:]
            
            if whole[0:6] == 'Degree':
                school = 'Second Degree From Same School'
            
            education.update({school: {'School Name': school, 'Degree': degree_name, 'Field of Study': field_of_study, 'Dates Attended': dates}})
    except TimeoutException:
        print('no education listed on profiled')


    body = driver.find_element_by_tag_name('main').find_elements_by_tag_name('div')[0].find_elements_by_tag_name('dd')
    header = body[0].text
    current_co = body[3].text.split('yrs')[0][:-3]
    location = body[2].text.split(' connections')[0][:-5]
    connections = body[2].text.split(' connections')[0][-5:]
    current_pos = body[3].text.split('mo')[0] + 'mos'
    LI_info_dict.update({person: {'Header': header, 'Current Company': current_co,
                          'Location': location, 'Connections': connections,
                          'Current Position': current_pos, 
                          'Past Experience': past_experience,
                          'Education': education}})
            
    return None
        
        
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
        except TimeoutException:
            search.clear()
            search.send_keys(name, '\ue007')
            print('searching "{name}"'.format(name=name))
            try:
                person = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div/div/div/div/div[2]/div/table/tbody/tr')))
                href = person.find_element_by_class_name('zp_yJfMM').find_element_by_class_name('zp_1sGdg').find_element_by_class_name('zp_EqOJn').find_element_by_class_name('zp_PrhFA').find_element_by_tag_name('a').get_attribute('href')
            except TimeoutException:
                print('{} not in Apollo database',format(name))
                href = 'Not in Apollo'
    except StaleElementReferenceException:
        search.clear()
        search.send_keys(name, ' ', location, '\ue007')
        print('searching "{name} {location}"'.format(name=name, location=location))
        try:
            person = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div/div/div/div/div[2]/div/table/tbody/tr')))
            href = person.find_element_by_class_name('zp_yJfMM').find_element_by_class_name('zp_1sGdg').find_element_by_class_name('zp_EqOJn').find_element_by_class_name('zp_PrhFA').find_element_by_tag_name('a').get_attribute('href')
        except TimeoutException:
            search.clear()
            search.send_keys(name, '\ue007')
            print('searching "{name}"'.format(name=name))
            try:
                person = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div/div/div/div/div[2]/div/table/tbody/tr')))
                href = person.find_element_by_class_name('zp_yJfMM').find_element_by_class_name('zp_1sGdg').find_element_by_class_name('zp_EqOJn').find_element_by_class_name('zp_PrhFA').find_element_by_tag_name('a').get_attribute('href')
            except TimeoutException:
                print('{} not in Apollo database',format(name))
                href = 'Not in Apollo'
    
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

def get_email(person, link):
    """
    

    Parameters
    ----------
    person: name of person
    link : link to person's Apollo.io page

    Returns
    -------
    None.

    """
    apollo_sign_in()
    driver.get(link)
    driver.maximize_window()
        
    access = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.zp-button:nth-child(2) > div:nth-child(2)")))
    access.click()
    time.sleep(5)
    email = driver.find_element_by_css_selector('.zp_3v1d1').text
    print(email)

#get_email('Jeff', 'https://app.apollo.io/#/people/54a286da7468693fda70cd29')
# m = 'https://app.apollo.io/#/people/60df94c1486e0d00012d1c98'
# get_email('Mike', m)    


    
# df = pd.DataFrame(out_dict).T
# df.to_excel('LISalesNavtest.xlsx')
    
    
# # apollo('John Smith')    
# urls = search(keywords = "God Seminary Bible", 
#                     # geography = ['Nashville, Tennessee, United States', 'Raleigh, North Carolina, United States'],
#                     # company = ['Bain Capital', 'Amazon Web Services'],
#                     industry = ['Nonprofit'],
#                     headcount = [1000, None],
#                     seniority = ['Partner', 'Owner', 'CXO', 'VP', 'Director'],
#                     # function = ['Accounting', 'Operations'],
#                     # title = ['President', 'Managing Director'],
#                     pages=11
#         )

# # # urls = ['https://www.linkedin.com/sales/search/people?companySize=F%2CG%2CH%2CI&doFetchHeroCard=false&industryIncluded=100&keywords=%27God%27%20OR%20%27seminary%27&logHistory=true&page=1&seniorityIncluded=9%2C10%2C8', 'https://www.linkedin.com/sales/search/people?companySize=F%2CG%2CH%2CI&doFetchHeroCard=false&industryIncluded=100&keywords=%27God%27%20OR%20%27seminary%27&logHistory=true&page=0&seniorityIncluded=9%2C10%2C8', 'https://www.linkedin.com/sales/search/people?companySize=F%2CG%2CH%2CI&doFetchHeroCard=false&industryIncluded=100&keywords=%27God%27%20OR%20%27seminary%27&logHistory=true&page=1&seniorityIncluded=9%2C10%2C8']
# for u in urls:
#     LI_href(u) 
#     time.sleep(5)
    
# print(len(names))
# with open ('LVPnames.json', 'w+') as f:
#     json.dump(names, f)
    
    
retries = {}
# # with open('LInames.json', 'r') as f:
# #     names = json.load(f)
# with open('LVPnames.json', 'r') as file:
#     names = json.load(file)   

# print(len(names))

s_counter = 0
f_counter = 0
for name in names:
    if name != 'all':
        data = names[name]
        url = data['href']
        try:
            LI_info(name, url)
            s_counter += 1
            print('successes = {}'.format(s_counter))
        except StaleElementReferenceException:
            retries[name] = url
            f_counter += 1
            print('failures = {}'.format(f_counter))
            continue
        except IndexError:
            print('empty profile')
        except TimeoutException:
            with open('LVPretries.json', 'w+') as fp:
                json.dump(retries, fp)
                
#             # print(out_dict)
#             with open('LVPfulldict.json', 'w+') as fw:
#                 json.dump(LI_info_dict, fw)
                
                
#             print('{} ppl to retry'.format(len(retries)))  
#             print('{} ppl succesfully saved'.format(len(LI_info_dict)))


# with open('LVPretries.json', 'w+') as fp:
#     json.dump(retries, fp)
    
# # print(out_dict)
# with open('LVPfulldict.json', 'w+') as fw:
#     json.dump(LI_info_dict, fw)
    
    
# print('{} ppl to retry'.format(len(retries)))  
# print('{} ppl succesfully saved'.format(len(LI_info_dict)))


# urls = search(keywords="'jesus' OR 'god' OR 'christ' OR 'theology' OR 'seminary'",
#        industry = ['Healthcare'],
#        headcount = [10000, None],
#        seniority = ['CXO', 'VP'],
#        geography = ['United States'],
#        pages = 2)


urls = ['https://www.linkedin.com/sales/search/people?companySize=G%2CH%2CI&doFetchHeroCard=false&geoIncluded=103644278&industryIncluded=139&keywords=%27jesus%27%20OR%20%27god%27%20OR%20%27christ%27%20OR%20%27theology%27%20OR%20%27seminary%27&logHistory=true&page=1&seniorityIncluded=8%2C7']
for u in urls:
    LI_href(u) 
    time.sleep(5)


s_counter = 0
f_counter = 0
for name in names:
    if name != 'all':
        data = names[name]
        url = data['href']
        try:
            LI_info(name, url)
            s_counter += 1
            print('successes = {}'.format(s_counter))
        except StaleElementReferenceException:
            retries[name] = url
            f_counter += 1
            print('failures = {}'.format(f_counter))
            continue
        except IndexError:
            print('empty profile')
        except TimeoutException:
            with open('LVPretries.json', 'w+') as fp:
                json.dump(retries, fp)
                
    
# with open('LVPfulldict.json', 'r') as file:
#     leads = json.load(file)

# print(len(leads))
# for human in leads:
#     data = leads[human]
#     company = data['Current Company'].split('at')[-1].split(',')[0]
#     location = data['Location'].split(' ')[0].split(',')[0]
#     try:
#         link = apollo_href(human, company, location)
#         print(human + ':' + link)
#         leads[human]['Apollo Link'] = link
#     # except TimeoutException:
#     #     leads[human]['Apollo Link'] = 'Not In Apollo'
#     #     print('{} not in apollo database'.format(human))
#     except ElementClickInterceptedException:
#         driver.close()
#         driver = webdriver.Firefox(firefox_profile=profile,
#                             desired_capabilities=desired)
#         continue

# with open('LVPfulldict.json', 'w') as fy:
#     json.dump(leads, fy)     
        
recruiter = 'https://www.linkedin.com/talent/hire/461102314/discover/recruiterSearch?searchContextId=f3181851-c6f5-484f-9848-88bc65e923c7&searchHistoryId=9475771844&searchRequestId=392c786a-d2b5-4601-9b41-35dbdfa90779&start=0'

     