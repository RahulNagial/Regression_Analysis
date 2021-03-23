#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 19:54:10 2021

@author: rahulnagial

This code scrapes data from rentfaster.ca for rental listings for the city of Calgary.
Idea is to use this information to build a model that can predict rental prices given different parameters.

"""

#  importing all the required libraries, using selenium for scraping
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

# starting time of code execution
start = time.time()

# clearing cache to ensure 'no memory left' error
# ref1: https://stackoverflow.com/questions/46529761/python-selenium-clearing-cache-and-cookies/47093059#47093059
# ref2: https://python-forum.io/Thread-Selenium-Webdriver-Memory-Problem 
profile = webdriver.FirefoxProfile()
profile.set_preference("browser.cache.disk.enable", False)
profile.set_preference("browser.cache.memory.enable", False)
profile.set_preference("browser.cache.offline.enable", False)
profile.set_preference("network.http.use-cache", False) 

# using Firefox geckodriver for scraping to avoid elementnotclickable errors encountered with chromedriver
browser = webdriver.Firefox(firefox_profile = profile,executable_path='/Users/rahulnagial/datascience/rentfasterscraping/geckodriver')
# going to the url containing listings
browser.get("https://www.rentfaster.ca/ab/calgary/rentals#dialog-listview")
# introducing impilicit wait to make driver wait before throwing up errors
browser.implicitly_wait(30)
# deleting all cookies
browser.delete_all_cookies()

# initializing data frame for storing final results 
df_rentfasterscraping = pd.DataFrame()

# wait 5 seconds to allow contents to load
time.sleep(5)
#  specifying no. of pages to be scrapes, ~1500 in this case
pages_to_scrape = 31

# main loop to iterate and access entries on each page 
for i in range(0, pages_to_scrape):
    # initializing list, data frame to store entries on each listing page
    df_temp = pd.DataFrame()
    Listings_Title = []
    Location = []
    Neighbourhood = []
    Fulldescription = []
    FlexTable_info = []
    MainTable_info =[]
    FeaturesTable_info =[]
    # finding all listing titles on a given page
    listings = browser.find_elements_by_class_name("listing-title")   
    # to keep track of number of listings covered on a given page
    count = 0
    #  loop going over each individual listing on a given page 
    for listing in listings:
        # breaking loop if last entry on the page reached
        if (count==48):
            break
        count += 1
        # printing for debugging, extracting all titles and appending to list
        print(listing.text)
        Listings_Title.append(listing.text)
        print(count)
        # allowing time for listing to load and then clicking on it
        time.sleep(1)
        listing.click()
        
        # getting address of listing
        try:
            location = browser.find_element_by_xpath('/html/body/div[4]/div[2]/div[3]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[2]/div[1]/div[3]')
            Location.append(location.text) 
        except:
            Location.append(-1)
        # getting name of neighbourhood located in 
        try:
            neighbourhood = browser.find_element_by_xpath('//*[@id="community-name"]')
            Neighbourhood.append(neighbourhood.text)
        except:
            Neighbourhood.append(-1)
        # getting full written description for a listing 
        try:
            fulldescription = browser.find_element_by_xpath('//*[@id="listingview_full_desc"]')
            Fulldescription.append(fulldescription.text)
        except:
            Fulldescription.append(-1)
        # getting building/community/property features mentioned at the end of each listing  
        try:
            featurestable_info = browser.find_element_by_xpath('/html/body/div[4]/div[2]/div[3]/div[2]/div/div[3]/div[1]/div[4]/div[2]/div')
            FeaturesTable_info.append(featurestable_info.text)
        except:
            FeaturesTable_info.append(-1)
        # getting information in top right corner such as listing ID, parking status, pet allowance etc.
        try:
            flextable_info = browser.find_element_by_xpath('/html/body/div[4]/div[2]/div[3]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[5]/ul')            
            FlexTable_info.append(flextable_info.text)
        except:
            FlexTable_info.append(-1)
        # getting no. of rows in the main table in listing mentioning type, rent, deposit, sq. ft, bedroom/baths etc.
        # ref: https://www.tutorialspoint.com/how-to-get-all-the-values-including-the-headers-inside-a-table-in-a-page-in-selenium-with-python
        rws = browser.find_elements_by_xpath("//table/tbody/tr")
        r = len(rws)
        row = []
        #iterating over the rows and copying mentioned info
        for i in range(1,r+1):
            d=browser.find_element_by_xpath("//table/tbody/tr["+str(i)+"]")
            row.append(d.text)        
        # getting information from the main table in listing mentioning type, rent, deposit, sq. ft, bedroom/baths etc.        
        try:
            MainTable_info.append(row)
        except:
            MainTable_info.append(-1)
        # closing a given listing after extracting information
        dismiss_button = browser.find_element_by_xpath('/html/body/div[4]/div[2]/button')
        time.sleep(1)
        dismiss_button.click()
        
    # saving information from all the listing on a given page (48 listings in total) in a dataframe
    df_temp['Listings_Title'] = Listings_Title
    df_temp['Location'] = Location
    df_temp['Neighbourhood'] = Neighbourhood
    df_temp['Fulldescription'] = Fulldescription
    df_temp['FlexTable_info'] = FlexTable_info
    df_temp['MainTable_info'] = MainTable_info
    df_temp['FeaturesTable_info'] = FeaturesTable_info
    # updating main dataframe storing final results, writing information in csv format after every page to avoid loss of information due to unexpected errors during execution 
    df_rentfasterscraping = pd.concat([df_rentfasterscraping, df_temp], ignore_index=True)
    df_rentfasterscraping.to_csv("/Users/rahulnagial/datascience/rentfasterscraping/rentfaster_scraped_data.csv", index=False)
    # moving on to next page and the loop continues 
    next_page = browser.find_element_by_xpath('//*[@id="modal-results-list"]/div[1]/span[1]/a')
    time.sleep(2)
    next_page.click()    
    time.sleep(5)

# taking end time to calculate effective time of execution of code
end = time.time()
# closing browser after completion
browser.quit()
