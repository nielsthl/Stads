#!/usr/bin/python
# -*- coding: utf-8 -*

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import sys
from bs4 import BeautifulSoup

class Stads(object):

    stadsurl = "https://istads.au.dk:443/stadsplus-master/faces/stadsplus-home.jsf"
    timeout = 20
    
    def __init__(self, userid, passwd, ikkeaktive=False):

        self.browser = webdriver.Chrome()
        self.login(userid, passwd)
        self.ikkeAktive = ikkeaktive

    def getloginpage(self):
        self.browser.get(Stads.stadsurl)
        try:
            element_present = EC.presence_of_element_located((By.ID, 'it1::content'))
            WebDriverWait(self.browser, Stads.timeout).until(element_present)
        except:
            print("Timed out waiting for login page to load")

    def login(self, userid, passwd):
        self.getloginpage()
        e1 = self.browser.find_element_by_id("it1::content")
        e1.send_keys(userid)
        e2 = self.browser.find_element_by_id("it2::content")
        e2.send_keys(passwd)

        buttone = self.browser.find_element_by_id("cb1")
        buttone.click()
        self.clicktoKarakterer()
 
    def switchtoFrame(self):
        try:
            element_present = EC.presence_of_element_located((By.ID, 'pt1:ifistads::f'))
            WebDriverWait(self.browser, Stads.timeout).until(element_present)
        except TimeoutException:
            print("Frame not present")

        self.browser.switch_to.frame("pt1:ifistads::f")

        
    def clicktoKarakterer(self):
        try:
            element_present = EC.presence_of_element_located((By.ID, 'pt1:topmenu4'))
            WebDriverWait(self.browser, Stads.timeout).until(element_present)
        except TimeoutException:
            print("Karakter button failed to show")
            
        buttone = self.browser.find_element_by_id("pt1:topmenu4")
        buttone.click()
        self.switchtoFrame()


    def clicktoNyStud(self):
         buttone= self.browser.find_element_by_id("button.nyStudButtonTable")
         buttone.click()
        

    def getKarakterer(self, studienr):
        try:
            element_present = EC.presence_of_element_located((By.ID, 'request_form'))
            WebDriverWait(self.browser, Stads.timeout).until(element_present)
        except TimeoutException:
            print("Karakterform time out")
        snr = self.browser.find_element_by_id("studienr")
        snr.send_keys(studienr)

# Medtag evt ikke aktive!

        if self.ikkeAktive:
            
            ikkeaktive = self.browser.find_element_by_id("ikkeAktive")
            ikkeaktive.click()
        
        buttone= self.browser.find_element_by_id("button.fremsogButtonTD")
        buttone.click()

        try:
            element_present = EC.presence_of_element_located((By.ID, 'RE100.navn.kolonne'))
            WebDriverWait(self.browser, Stads.timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
            
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')

        def formtxt(web):
            return (web.text.strip('\n'))

        stadskoder = map(formtxt, soup.find_all(id="RE100.kode.kolonne"))
        kurser= map(formtxt, soup.find_all(id="RE100.navn.kolonne"))
        karakterer = map(formtxt, soup.find_all(id="RE100.karakter.kolonne"))
        datoer = map(formtxt, soup.find_all(id="RE100.bedoemDate.kolonne"))

        #
        # Reformat dates to US format for sorting.
        #

        def datoswap(da):
            str = da.split(".")
            return str[2]+"."+str[1]+"."+str[0]

        datoer = map(datoswap, datoer)
        samlet = list(zip(stadskoder, kurser, karakterer, datoer))
        samlet.sort(key = lambda v: v[3]) # sort according to date, earliest on top

        self.clicktoNyStud()
        
        return samlet # zip(stadskoder, kurser, karakterer, datoer)
        

    def quit(self):
        self.browser.quit()
