from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import csv
from get_location import get_long_lat
import settings
from bs4 import BeautifulSoup



driver = webdriver.Chrome('./chromedriver.exe')
wait = WebDriverWait(driver , 600)


seen = {}

def write_file(file_name , page):
    with open(file_name, "w", encoding="utf-8") as f:
            f.write(str(page))


def get_page_source(url):
    driver.get(settings.BASE_URL + url) 

    html_source_code = driver.execute_script("return document.body.innerHTML;").encode("utf-8")
    return html_source_code
    
def create_resturants_csv():
    file_path = 'resturants.csv'
    with open(file_path, 'w', encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['link' ,'background_image','icon', 'name', 'description', 'rate' , "lat" , "lng" , "address" , "zone"])




def get_page_number(url):
    n = url.split("&")[-1].split("=")[-1]
    return int(n)


def log_returants(resturants):
    file_path = 'resturants.csv'
    with open(file_path, 'a', encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        for resturant in resturants:
            writer.writerow([
                resturant["link"] , resturant['background_image'] ,resturant['icon'], 
                resturant['name'], resturant['description'], resturant['rate'] , resturant["lat"] , resturant["lng"]
                ])
    

def get_resturants(url):
    global seen

    city_name = url.split("/")[1]
    html_source_code = get_page_source(url)

    soup = BeautifulSoup(html_source_code, 'lxml')
    




    resturants_soup = soup.find("main" , {"class" : "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"})

    resturants_soup = resturants_soup.findChildren("a" , recursive=False)

    resturants = []
    for resturant_soup in resturants_soup:
        link = resturant_soup["href"]
        article = resturant_soup.contents[0]

        background_image = article.contents[0].find("img")["src"]
        icon = article.contents[0].find("div").find("img")["src"]
        name = article.contents[1].contents[0].contents[0].find('h1').text

        if seen.get(name ,-1) == 1:
            continue

        rate = article.contents[1].contents[0].contents[1].find('span').text
        description = article.contents[1].contents[0].contents[0].find('p').text

        try:
            location = "مطعم " + name +  " " + city_name + " السعودية"
            lat  , lng = get_long_lat(location)
        except:
            lat , lng = 0 , 0

        zone = url.split("/")[2]
        address = url.split("/")[1] + " " + zone
        resturant = {
            "link" : link,
            "background_image" : background_image,
            "icon" : icon,
            "name": name,
            "description" : description,
            "rate" : rate,
            "lat" : lat,
            "lng" : lng,
            "address":address,
            "zone" : zone
        }
        
        resturants.append(resturant)
        seen[name] = 1
    
    log_returants(resturants)
    # write_file('source.txt' , names)


    ############
    footer_soup = soup.find("footer" , {"class" : "mt-12"}).contents[0]
    footer_links = footer_soup.findChildren("a" , recursive=False)
    last_url = footer_links[-1]["href"]
    print("footer length" , len(footer_links))
    print(last_url)
    current_page = get_page_number(url)
    last_page = get_page_number(last_url)
    if current_page < last_page:
        next_url = url.replace(f"page={current_page}" , f"page={current_page+1}")
        get_resturants(next_url)

        
    print("page number" , get_page_number(last_url))
    ###########
    
