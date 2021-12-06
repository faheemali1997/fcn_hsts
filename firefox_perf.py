from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import csv
import time
import pandas as pd

fields = ['Domain Name', 'Page Load Time', 'Request Response Time', 'Page Render Time', 'isHSTSEnabled']

csvfile, writer = None, None
csvfile  = open("mozilla.csv", 'w')
writer = csv.writer(csvfile)
writer.writerow(fields)


def performance_test(website):


    page_load_time, request_response_time, renderTime = 0,0,0
    hyperlink = "https://www.{}".format(website)
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
    firefox_profile.set_preference("browser.cache.disk.enable", False)
    firefox_profile.set_preference("browser.cache.memory.enable", False)
    firefox_profile.set_preference("browser.cache.offline.enable", False)
    firefox_profile.set_preference("network.http.use-cache", False)
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_profile=firefox_profile)
    driver.set_page_load_timeout(30)

    try:
        driver.get(hyperlink)
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
                print("Sleeping for 1 second")
                time.sleep(1)
                csvfile = open("mozilla.csv", 'a')
                writer = csv.writer(csvfile)
        try:
            result = performance_test(domain[0])
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
