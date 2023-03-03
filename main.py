from selenium_utils import create_resturants_csv , get_resturants , create_links_resturants_csv
import csv


def logs(line):
    line += '\n'
    file_path = 'logs.txt'
    with open(file_path, 'a', encoding='UTF-8') as f:
        f.write(line)


if __name__ == "__main__":
  # url = "restaurants/%D8%A8%D8%AD%D8%B1%D9%8A%D9%86/%D8%A7%D9%84%D9%85%D8%AD%D8%B1%D9%82?lat=26.2504534&lng=50.6100213&page=1"
  # url = "restaurants/riyadh/riyadh?lat=24.7135517&lng=46.6752957&page=1"
  create_resturants_csv()
  create_links_resturants_csv()
  file_name = "jaddah.csv"

  with open(file_name, 'r' , encoding="utf-8") as data:
    for line in csv.DictReader(data):
      try:
        get_resturants(line["url"])
        logs(line["url"])
      except:
         logs(line["url"] + "#"*20)