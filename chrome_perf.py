import csv
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

fields = ['Domain Name', 'Page Load Time', 'Request Response Time', 'Page Render Time', 'isHSTSEnabled']

csvfile, writer = None, None
csvfile  = open("chrome.csv", 'w')

writer = csv.writer(csvfile)
writer.writerow(fields)


def get_page_load(website, use_http=None):
    
    hyperlink = "https://www.{}".format(website)
    options = Options()
    #options.add_argument("--headless")
    options.add_argument("--disable-application-cache")
    options.add_argument("--incognito")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    page_load_time, request_response_time, renderTime = 0,0,0
    
    try:
        driver.get(hyperlink)
        print("Link %s" % hyperlink)
        timing = driver.execute_script("return window.performance.timing") 
        ''' Calculate the performance'''
        page_load_time = timing['loadEventEnd'] - timing['responseEnd']
        request_response_time = timing['responseEnd'] - timing['requestStart']
        renderTime = timing['domComplete'] - timing['domLoading']
        
        print("Page Load Time: %s" % page_load_time)
        print("Request Response Time: %s" % request_response_time)
        print("Page Render Time: %s" % renderTime)
        
    finally:
        driver.quit()
        return [page_load_time, request_response_time, renderTime]


try:
    f = open("output.txt","r")
    websites = f.readlines()
    for idx, w in enumerate(websites):
        domain = w.strip().split(":")
        if (idx+1)%10 == 0:
                csvfile.close()
                print("Sleeping for some time")
                time.sleep(2)     
                csvfile = open("chrome.csv", 'a')
                writer = csv.writer(csvfile)
        try:
            result = get_page_load(domain[0])
            writer.writerow([domain[0]] + result + [int(domain[1])])

        except Exception as e:
            writer.writerow([domain[0],0,0,0,int(domain[1])])
            continue
except KeyboardInterrupt:
    print("Interrupt from keyboard")
except:
    print("Other exception")
finally:
    csvfile.close()
'''
