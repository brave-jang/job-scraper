"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
import requests
import csv
from flask import Flask, render_template, request, send_file, redirect
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

def stack_url(word):
    return f'https://stackoverflow.com/jobs?r=true&q={word}'

def wework_url(word):
    return f'https://weworkremotely.com/remote-jobs/search?term={word}'

def remote_url(word):
    return f'https://remoteok.io/remote-{word}-jobs'

def bs_soup(url):
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text, "html.parser")
    return soup

def save_to_file(word, jobs):
    file = open(f"{word}.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["Title","company","link"])
    for job in jobs:
        writer.writerow(list(job.values()))
    return

app = Flask("Remote Jobs")

db = {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search")
def search():
    posts = []
    jobs = {}
    info = request.args.get('word')

    stack_url_detail = stack_url(info)
    wework_url_detail = wework_url(info)
    remote_url_detail = remote_url(info)

    stack_info =  bs_soup(stack_url_detail).find_all("div", {"class":"fl1"})
    wework_info = bs_soup(wework_url_detail).find_all("li", {"class":"feature"})
    remote_info = bs_soup(remote_url_detail).find_all("td", {"class":"company_and_position"})

    stack_jobs = "https://stackoverflow.com"
    wework_jobs = "https://weworkremotely.com"
    remote_jobs = "https://remoteok.io"

    info = info.lower()
    fromDb = db.get(info)

    if fromDb:
        posts = fromDb
    else:
        for stack in stack_info:
            try:
                company_url = stack.find("a")["href"]
                if company_url != "#":
                    title = stack.find("h2", {"class":"fc-black-800"})
                    company_name = stack.find("h3").find("span")
                    jobs_url = stack_jobs + company_url
                    jobs = {
                        "title" : title.text,
                        'name' : company_name.text,
                        'url' : jobs_url,
                    }
                    posts.append(jobs)
                    db[info] = posts
            except:
                pass

        for wework in wework_info:
            try:
                try:
                    company_url = wework.find("div", {"class":"tooltip"}).next_sibling["href"]
                    company_name = wework.find("span", {"class":"company"})
                    title = wework.text
                    jobs_url = wework_jobs + company_url
                except:
                    company_url = wework.find("a")["href"]
                    company_name = wework.find("span", {"class":"company"})
                    title = wework.text
                    jobs_url = wework_jobs + company_url
                jobs = {
                    'title' : title,
                    'name' : company_name.text,
                    'url' : jobs_url
                }
                posts.append(jobs)
                db[info] = posts
            except:
                pass

        for remote in remote_info:
            try:
                company_name = remote.find("h3")
                title = remote.text
                company_url = remote.find("a")["href"]
                jobs_url = remote_jobs + company_url
                jobs = {
                    'title' : title,
                    'name' : company_name.text,
                    'url' : jobs_url
                }
                posts.append(jobs)
                db[info] = posts
            except:
                pass
    return render_template("search.html", posts=posts, info=info)

@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(word, jobs)
        return send_file(f'{word}.csv',mimetype = "text/csv",attachment_filename = f"{word}.csv",as_attachment = True
)
    except:
        return redirect("/")

app.run(host="0.0.0.0")