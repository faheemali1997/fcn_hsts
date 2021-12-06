import csv

from selenium import webdriver

import time


fields = ['Domain Name', 'Page Load Time','Request Response Time', 'Page Render Time',  'isHSTSEnabled']

filename = "website_perf.csv"


def perf_test(website):

    hyperlink = "https://www." + website

    print("*******************")

    print(hyperlink)

    driver = webdriver.Safari()

    driver.set_page_load_timeout(20)

    page_load_time = -1

    request_response_time = -1

    renderTime = -1

    try: 
        driver.get(hyperlink)

        time.sleep(5)

        loadEventEnd = driver.execute_script("return window.performance.timing.loadEventEnd")

        loadEventStart = driver.execute_script("return window.performance.timing.loadEventStart")
        
        responseEnd = driver.execute_script("return window.performance.timing.responseEnd")
        
        requestStart = driver.execute_script("return window.performance.timing.requestStart")
        
        domComplete = driver.execute_script("return window.performance.timing.domComplete")
        
        domLoading = driver.execute_script("return window.performance.timing.domLoading")

        navigationStart = driver.execute_script("return window.performance.timing.navigationStart")

        ''' Calculate the performance'''

        page_load_time = loadEventEnd - loadEventStart

        request_response_time = responseEnd - requestStart

        renderTime = domComplete - domLoading

    finally:

        print("Page Load Time: %s" % page_load_time)

        print("Request Response Time: %s" % request_response_time)

        print("Page Render Time: %s" % renderTime)

        driver.quit()

        return [page_load_time, request_response_time, renderTime]






with open(filename, 'w') as csvfile: 
# creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
    
# writing the fields 
    csvwriter.writerow(fields) 


    with open("websites.txt") as f:
        
        for line in f:
            
            domain = line.strip().split(":")
            #print(domain)
            
            csvwriter.writerow([domain[0]] + perf_test(domain[0]) + [domain[1]])




'''
def perf_test(website):

    hyperlink = "https://www." + website  

    driver = webdriver.Safari()

    driver.get(hyperlink)

    timing = driver.execute_script("return window.performance.timing")
     
    page_load_time = timing['loadEventEnd'] - timing['responseEnd']

    request_response_time = timing['responseEnd'] - timing['requestStart']

    renderTime = timing['domComplete'] - timing['domLoading']

    driver.quit()

    print(hyperlink)

    print("Page Load Time: %s" % page_load_time)

    print("Request Response Time: %s" % request_response_time)

    print("Page Render Time: %s" % renderTime)

    return [page_load_time, request_response_time, renderTime]
'''  
