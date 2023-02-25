from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import csv
import requests
import settings
from bs4 import BeautifulSoup



driver = webdriver.Chrome('./chromedriver.exe')
wait = WebDriverWait(driver , 600)




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
        writer.writerow(['link' ,'background_image','icon', 'name', 'description', 'rate'])




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
                resturant['name'], resturant['description'], resturant['rate']
                ])
    

def get_resturants(url):
    

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
        rate = article.contents[1].contents[0].contents[1].find('span').text
        description = article.contents[1].contents[0].contents[0].find('p').text

        resturant = {
            "link" : link,
            "background_image" : background_image,
            "icon" : icon,
            "name": name,
            "description" : description,
            "rate" : rate
        }

        resturants.append(resturant)

    
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
    
if __name__ == "__main__":
    # url = "restaurants/%D8%A8%D8%AD%D8%B1%D9%8A%D9%86/%D8%A7%D9%84%D9%85%D8%AD%D8%B1%D9%82?lat=26.2504534&lng=50.6100213&page=1"
    url = "restaurants/riyadh/riyadh?lat=24.7135517&lng=46.6752957"
    # url = "restaurants/بحرين/المحرق?lat=26.2504534&lng=50.6100213"
    create_resturants_csv()
    get_resturants(url)

    # next_btn =  WebDriverWait(driver, 10).until(
    #                 EC.presence_of_element_located((By.XPATH , '//*[@id="__next"]/main/section/footer/div/a[5]'))
    #             ).text
    

    # print(next_btn)
