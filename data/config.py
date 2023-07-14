import json

test = {1: "кот", 2: "жмых"}
test_2 = {1: ('/test?theme=289', '/test?theme=354'),
          2: ('/test?theme=342', '/test?theme=355'), 3: ('/test?theme=258', '/test?theme=356')}
answer = []
with open("russian/tasks_links.json") as file:
    tasks_links = json.load(file)


def get_info(links):
    number = 1
    while number <= len(links):
        for task in links.get(str(number)):
            print(task)
        number += 1


print(get_info(tasks_links))


# for page in selenium_pages:
#     soup = BeautifulSoup(page, "lxml")
#     for task_id in soup.find_all("div", {"class": "problem_container"}, id=True):
#         all_tasks.append(task_id.get("id").replace("problem_", ""))
#
#
# for task in all_tasks:
#     if soup.find("div", class_="probtext") is None:
#         current_id = "sol" + str(task)
#         r = requests.get("https://rus-ege.sdamgia.ru/problem?id=" + str(task))
#         soup = BeautifulSoup(r.text, "lxml")
#         number += 1
#         head = soup.find("div", class_="pbody").get_text().replace("\u202f", " ").replace("\xa0", " ")
#         answer = soup.find("div", class_="solution", id=current_id).find_next_sibling().get_text()
#         solution = soup.find("div", {"class": "solution"},
#                              id=current_id).get_text().replace("\u202f", " ").replace("\xa0", " ")
#         content = {
#             "number": number,
#             "head": head,
#             # "text": text,
#             "answer": answer,
#             "solution": solution
#         }
#     else:
#         current_id = "sol" + str(task)
#         r = requests.get("https://rus-ege.sdamgia.ru/problem?id=" + str(task))
#         soup = BeautifulSoup(r.text, "lxml")
#         number += 1
#         head = soup.find("div", class_="pbody").get_text().replace("\u202f", " ").replace("\xa0", " ")
#         text = soup.find("div", class_="probtext").get_text().replace("\u202f", " ").replace("\xa0", " ")
#         answer = soup.find("div", class_="solution", id=current_id).find_next_sibling().get_text()
#         solution = soup.find("div", {"class": "solution"},
#                              id=current_id).get_text().replace("\u202f", " ").replace("\xa0", " ")
#         content = {
#             "number": number,
#             "head": head,
#             "text": text,
#             "answer": answer,
#             "solution": solution
#         }
#
#     print(content)
#
# print(all_tasks)