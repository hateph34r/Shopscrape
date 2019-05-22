#! /usr/bin/env python3
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import os

def csvFileReader(filename):
  """This function opens the CSV, grabs the data and closes the CSV file"""
  try:
    with open(filename) as csv_file:
      data = csv.reader(csv_file)
      imported = []
      for row in data:
        imported.append(row)
    list = [l[1] for l in imported]
    csv_file.closed
    return imported[1:]
  except:
    return None
    
def startBrowser(foldername):
"""This function starts and returns a Chromedriver web browser that the app will use to create Google searches to find PDF Maps."""
  chrome_profile = webdriver.ChromeOptions()
  download ="C:\\Users\\JGardner\\Downloads\\"+foldername
  profile = {"download.default_directory" : download, "plugins.plugins_disabled": ["Chrome PDF Viewer"]}
  chrome_profile.add_experimental_option("prefs",profile)
  browser = webdriver.Chrome(chrome_options=chrome_profile)
  browser.implicitly_wait(30)
  return browser
  
def getPDF(url,foldername):
"""This function calls startBrowser to start a chromedriver browser, navigates to Google and searches for a PDF map of a given shopping area, downloading any PDFs that return as results."""
  browser = startBrowser(foldername)
  browser.get(url)
  time.sleep(15)
  count = 1
  while count <=10:
    xpath = '//*[@id="rso"]/div/div/div['+str(count)+']/div/h3/a'
    try:
      browser.find_element_by_xpath(xpath).click()
    except:
      print ('Link ' +str(count)+ ' not found')
    if browser.current_url != url:
      browser.get(url)
      time.sleep(10)
    count = count+1
  dcomplete = False
  while dcomplete==False:
    count2 = 0
    list = os.listdir(foldername)
    if list == []:
      dcomplete = True
    for file in list:
      length = len(str(file))
      type = length -4
      print(file[type:])
      if file[type:].lower()=='.pdf':
        print('total finished: '+str(count2))
        count2 = count2+1
      if count2 ==len(list):
        print('total finished: '+str(count2))
        print('downloads finished!')
        dcomplete = True
  browser.quit()
  return True
 
def main():
  filename = 'dev_shopping_T1s.csv'
  if (csvFileReader(filename) == None):
    return print("Cannot find file " +filename)
  else:
    for item in csvFileReader(filename):
      t = [i.replace(' ','+') for i in item]
      url = '+'.join([t[2],t[3],t[4],t[5],'map','inurl%3Apdf'])
      furl = 'https://www.google.com/#safe=off&q='+url
      foldername ="Splaces scrape\\"+' '.join([item[2],item[4],item[5]])
      print(foldername)
      print(furl)
      if os.path.exists(foldername):
        print ('Directory already exists')
      if not os.path.exists(foldername):
        os.makedirs(foldername)
        print('created folder '+foldername)
      getPDF(furl, foldername)
      numfile = len(os.listdir(foldername))
      if numfile <=5:
        url = '+'.join([t[2],t[4],t[5],'map','inurl%3Apdf'])
        furl = 'https://www.google.com/#safe=off&q='+url
        getPDF(furl,foldername)
        

main()
