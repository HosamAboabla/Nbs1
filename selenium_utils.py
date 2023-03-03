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
from random import randint
import datetime

driver = webdriver.Chrome('./chromedriver.exe')
wait = WebDriverWait(driver , 600)

res_id = 14
seen = {}



def timestamp():
    return str(datetime.datetime.now())


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return str(randint(range_start, range_end))


def write_file(file_name , page):
    with open(file_name, "w", encoding="utf-8") as f:
            f.write(str(page))


def get_page_source(url):
    driver.get(settings.BASE_URL + url) 

    html_source_code = driver.execute_script("return document.body.innerHTML;").encode("utf-8")
    return html_source_code
    

def create_resturants_csv():
    file_path = 'files/resturants.csv'
    with open(file_path, 'w', encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow([
            "id","name","phone","email","logo","latitude","longitude","address","footer_text","minimum_order",
            "comission","schedule_order","status","vendor_id","created_at","updated_at","free_delivery",
            "rating","cover_photo","delivery","take_away","item_section","tax","zone_id","reviews_section",
            "active","off_day","gst","self_delivery_system","pos_system","minimum_shipping_charge","delivery_time",
            "veg","non_veg","order_count","total_order","module_id","order_place_to_schedule_interval","featured",
            "per_ke_shipping_charge"
            ])


def create_links_resturants_csv():
    file_path = 'files/links_resturants.csv'
    with open(file_path, 'w', encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow([
            "id", "name", "link", "background_image", 
            "icon", "description", "rate","logo","cover_photo"
            ])
        


def get_page_number(url):
    n = url.split("&")[-1].split("=")[-1]
    return int(n)


def log_returants(resturants):
    file_path = 'files/resturants.csv'
    with open(file_path, 'a', encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        for resturant in resturants:
            writer.writerow([
                resturant["id"],resturant["name"],resturant["phone"],None,resturant["logo"],resturant["latitude"],resturant["longitude"]
                ,resturant["address"],"NULL","0","NULL","0","1","7","NULL","NULL","0",
                "NULL",resturant["cover_photo"],"1","1","1","0",
                "6", # zone_id
                "1",
                "1",None,"NULL","0","0","0","30-40",
                "1","1","0","0",
                "1", # module_id
                "0","0","0"
            ])

def log_links_returants(links_resturants):
    file_path = 'files/' + 'links_resturants.csv'
    with open(file_path, 'a', encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        for resturant in links_resturants:
            writer.writerow([
                resturant["id"],resturant["name"],resturant["link"],resturant["background_image"],
                resturant["icon"],resturant["description"],resturant["rate"], resturant["logo"],resturant["cover_photo"],
            ])



def check_if_exists():
    with open("resturants_last.csv", 'r' , encoding="utf-8") as data:
        for line in csv.DictReader(data):
            get_resturants(line["url"])
    return 1

def get_resturants(url):
    global seen , res_id


    city_name = url.split("/")[1]
    html_source_code = get_page_source(url)

    soup = BeautifulSoup(html_source_code, 'lxml')
    




    resturants_soup = soup.find("main" , {"class" : "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"})

    resturants_soup = resturants_soup.findChildren("a" , recursive=False)

    resturants = []
    links_resturants = []
    for resturant_soup in resturants_soup:
        link = resturant_soup["href"]
        article = resturant_soup.contents[0]

        name = article.contents[1].contents[0].contents[0].find('h1').text
        zone = url.split('/')[2].split("?")[0]
        address = url.split("/")[1] + " " + zone

        if seen.get(name+address+zone ,-1) == 1:
            continue

        background_image_url = article.contents[0].find("img")["src"]
        icon_url = article.contents[0].find("div").find("img")["src"]
        rate = article.contents[1].contents[0].contents[1].find('span').text
        description = article.contents[1].contents[0].contents[0].find('p').text


        try:
            location = "مطعم "+ name + " " + address + " السعودية"
            lat  , lng = get_long_lat(location)
        except:
            lat , lng = 0 , 0

        resturant_phone = random_with_N_digits(10)
        cover_photo     = f"{res_id}_background.png"
        logo            = f"{res_id}_icon.png"
        resturant = {
            "id" : res_id,
            "name": name,
            "phone" : resturant_phone,
            "logo" : logo,
            "latitude" : lat,
            "longitude" : lng,
            "address" : address,
            "cover_photo" : cover_photo,
        }
        
        link_res = {
            "id" : res_id,
            "name": name,
            "link" : link,
            "background_image" : background_image_url,
            "icon" : icon_url,
            "description" : description,
            "rate" : rate,
            "logo" : logo,
            "cover_photo" : cover_photo,
        }

        resturants.append(resturant)
        links_resturants.append(link_res)
        res_id += 1
        seen[name+address+zone] = 1
    
    log_returants(resturants)
    log_links_returants(links_resturants)
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
    
