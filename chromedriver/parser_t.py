# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup
# from selenium.webdriver.chrome.service import Service
# import json
# # Set up Chrome WebDriver
# service = Service(ChromeDriverManager(version="114.0.5735.90").install())
# options = webdriver.ChromeOptions()
#
# driver = webdriver.Chrome(options=options, service=service)
#
# # Load the webpage
# url = 'https://rus-ege.sdamgia.ru/prob-catalog'
# driver.get(url)
#
#
# # Get the page source
# page_source = driver.page_source
#
# links_list = []
# # Create a BeautifulSoup object with the page source
# soup = BeautifulSoup(page_source, 'html.parser')
# task_number = 1  # для ключей словаря
# for i, task in enumerate(soup.find_all("div", class_="Theme nobg"), start=1):
#     task_link = task.find("a", class_="Theme-link").get('href')
#     links_list.append((i, task_link))
# print(links_list)
# links = {}
# for link in links_list:
#     if len(links) == 27:
#         break
#     links.update([link])
# with open("russian_links_2907.json", "w") as file:
#     json.dump(links, file, indent=4, ensure_ascii=False)
#
#
# # Close the WebDriver
# driver.quit()


a_string = "Прекрасная Катя"


def formatting(string):
    return string.replace("Катя", "Катя, я люблю тебя").replace("Прекрасная", "Замечательная")


rus_task_8_rubbish = "<br/><br/><td style=\"text-align:center;width:45px\">А</td>" \
             "<td style=\"text-align:center;width:45px\">Б</td><td " \
             "style=\"text-align:center;width:45px\">В</td><td style=\"text-align:" \
             "center;width:45px\">Г</td><td style=\"text-align"\
             ":center;width:45px\">Д</td><td style=\"height:14px\"> </td>" \
             "<td style=\"height:14px\"> </td><td style=\"height:14px\">"\
             " </td><td style=\"height:14px\"> </td><td style=\"height:14px\"> </td>"
print(formatting(a_string))
