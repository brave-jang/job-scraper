import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


def stack_url(word):
    return f'https://stackoverflow.com/jobs?r=true&q={word}'

def wework_url(word):
    return f'https://weworkremotely.com/remote-jobs/search?term={word}'

def remote_url(word):
    return f'https://remoteok.io/remote-{word}-jobs'


stack_url_detail = stack_url('python')
wework_url_detail = wework_url('python')
remote_url_detail = remote_url('python')


def bs_soup(url):
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text, "html.parser")
    return soup


stack_info =  bs_soup(stack_url_detail).find_all("div", {"class":"fl1"})
wework_info = bs_soup(wework_url_detail).find_all("li", {"class":"feature"})
remote_info = bs_soup(remote_url_detail).find_all("td", {"class":"company_and_position"})


stack_jobs = "https://stackoverflow.com"
wework_jobs = "https://weworkremotely.com"
remote_jobs = "https://remoteok.io"


for info in stack_info:
    try:
        info_link = info.find("a")["href"]
        if info_link != '#':
            info_company = info.find("h3").find("span")
            info_title = info.find("h2", {"class":"fc-black-800"})
            print(info_title)
            print(info_link)
            print(info_company)
    except:
        pass


# for info in wework_info:
#     try:
#         link = info.find("div", {"class":"tooltip"}).next_sibling["href"]
#         name = info.find("span", {"class":"company"})
#     except:
#         link = info.find("a")["href"]
#         name = info.find("span", {"class":"company"})
#     print(link, name.text)

# for info in remote_info:
#     try:
#         name = info.find("h3")
#         link = info.find("a")["href"]
#         info_link = remote_jobs + link
#         print(info_link)
#         print(type(info_link))
#         print(name.text)
#     except:
#         pass