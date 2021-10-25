from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from datetime import datetime as dt
from time import sleep
import time
import requests
import random
from bs4 import BeautifulSoup
import sys



headers = {
'Accept-Encoding': 'gzip, deflate, sdch',
'Accept-Language': 'en-US,en;q=0.8',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Referer': 'http://www.wikipedia.org/'
}



def get_random_proxy(headers):
    url = 'https://www.sslproxies.org/'
    random_ip = []
    random_port = []

    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Get the Random IP Address
    for x in soup.findAll('td')[::8]:
        random_ip.append(x.get_text())

    # Get Their Port
    for y in soup.findAll('td')[1::8]:
        random_port.append(y.get_text())

    # Zip together
    z = list(zip(random_ip, random_port))

    # This will Fetch Random IP Address and corresponding PORT Number
    number = random.randint(0, len(z)-50)
    ip_random = z[number]

    # convert Tuple into String and formart IP and PORT Address
    ip_random_string = "{}:{}".format(ip_random[0],ip_random[1])

    # Create a Proxy
    proxy =    {'http':ip_random_string}

    return proxy

def get_viable_proxy_list(headers, list_length):
    proxy_list = []
    url = 'https://httpbin.org/ip'

    for i in range(list_length):
        #Keep attempting to establish a connection until a viable proxy is found
        proxy_found = False
        while not proxy_found:
            try:
                proxy = get_random_proxy(headers)
                response = requests.get(url, proxies=proxy, timeout=4)
                print(f"ACCESSING URL WITH PROXY: {proxy}")
                if response != None:
                    proxy_found = True
                    print(f"FOUND VIABLE PROXY #{i+1}")
                    proxy_list.append(proxy)
                break
            except:
                pass


    return proxy_list


# timestamp = time.time()
# sleep(1)
# time_elapsed = time.time() - timestamp
# print(time_elapsed)


# url = 'https://www.ebay.com/itm/392950815798'
#BRUTE FORCE - SELENIUM
# for i in range(1000):
#     driver = webdriver.Chrome()
#     driver.get(url)
#     print(f"VISIT #{i+1} to {url} COMPLETE")
#     sleep(random.randint(1,3))
#     driver.close()

#Proxy-based - Selenium
# View efficiency (9-30-20): 1000 views over 4 instances; +743
def bulk_listing_visits(url='https://whatismyipaddress.com/', view_count=100):

    proxy_list = get_viable_proxy_list(headers=headers, list_length=10)

    for i in range(view_count):
        if i%500 == 0 and i != 0:
            print("\n\nRETRIEVING NEW PROXY LIST\n\n")
            proxy_list = get_viable_proxy_list(headers=headers, list_length=10)

        proxy = proxy_list[random.randint(0, len(proxy_list)-1)]

        
        chrome_options = webdriver.ChromeOptions()
        # if 'facebook' not in url:
        #     chrome_options.add_argument('--headless')
        chrome_options.add_argument(f"--proxy-server={proxy['http']}")


        try:
            driver = webdriver.Chrome(executable_path='C:/Users/emman/Desktop/chromedriver.exe', options=chrome_options)
            driver.minimize_window()
            driver.set_page_load_timeout(10)
            driver.get(url)
            print(f"VISIT #{i+1} to {url} COMPLETE USING PROXY: {proxy}")
            sleep(1.5)

        except:
            print(f"REMOVING THE FOLLOWING PROXY: {proxy}")
            proxy_list.remove(proxy)
            new_proxy = get_viable_proxy_list(headers=headers, list_length=1)[0]
            proxy_list.append(new_proxy)

        #Repeatedly attempts to close the browser until close is successful
        while True:
            try:
                driver.close()
                break
            except:
                pass


##Proxy-based
# proxy_list = get_viable_proxy_list(headers=headers, list_length=5)
#
# for i in range(10000):
#     if i%500 == 0 and i != 0:
#         print("\n\nRETRIEVING NEW PROXY LIST\n\n")
#         proxy_list = get_viable_proxy_list(headers=headers, list_length=5)
#     proxy = proxy_list[random.randint(0, len(proxy_list)-1)]
#     try:
#         response = requests.get(url, proxies=proxy, headers=headers, timeout=4)
#         print(f"VISIT #{i+1} to {url} COMPLETE: {response}")
#     except:
#         print(f"REMOVING THE FOLLOWING PROXY: {proxy}")
#         proxy_list.remove(proxy)
#         new_proxy = get_viable_proxy_list(headers=headers, list_length=1)[0]
#         proxy_list.append(new_proxy)

if __name__ == '__main__':
    args = sys.argv[1] if len(sys.argv) > 1 else None

    if args == None:
        bulk_listing_visits()

    #Enter link and desired viewcount
    #python {script} {url} {viewcount}
    elif 'http' in args:
        bulk_listing_visits(url=args, view_count=int(sys.argv[2]))
