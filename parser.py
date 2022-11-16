from bs4 import BeautifulSoup
import requests

# занести в словарь номер задания, вопрос, текст и ответ

url = "https://rus-ege.sdamgia.ru/test?theme=289"
r = requests.get(url)
soup = BeautifulSoup(r.text, "lxml")
result_heads = []
headers_list = []
content = {}
# for headers in soup.find_all("p"):
#     headers_list.append(headers.get("left_margin"))
for heads in soup.find_all("p"):
    head = soup.find("p", {"class": "left_margin"})
    corrected_head = str(head).replace("</p>", "")
    result_heads.append(corrected_head)
    content[heads] = {
        "head": head
    }
print(content)
# test123
