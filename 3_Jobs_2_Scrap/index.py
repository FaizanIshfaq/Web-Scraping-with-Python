# imports
import requests
from bs4 import BeautifulSoup

WEB_URL = "https://m.timesjobs.com/mobile/jobs-search-result.html?jobsSearchCriteria=Information%20Technology&cboPresFuncArea=35"
WEB_CLASS = "srp-listing  clearfix "

def fetch_url_data(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response

def check_status(response):
    return response.status_code == 200

def find_jobs_details(soup):
    jobs = soup.find_all('li')
    all_jobs = []

    for job in jobs:
        box = job.find('div', class_='srp-listing')
        if not box:
            continue  
        try:
            job_data = parse_html(box)
            all_jobs.append(job_data)
            
        except AttributeError:
            continue 

    return all_jobs

def parse_html(box):
    
    title = box.find('h3').get_text(strip=True)
    company_name = box.find('span', class_="srp-comp-name").get_text(strip=True)
    posting_time = box.find('span', class_="posting-time").get_text(strip=True)

    # skills_div = box.find('div', class_="srp-keyskills")
    # skills = skills_div.find_all('a')
    # skills_required = [skill.get_text(strip=True) for skill in skills]

    skills = box.find('div',class_="srp-keyskills")
    skills = skills.find_all('a')
    skills_required = []
    
    for skill in skills:
        skills_required.append(skill.get_text(strip = True))
        
    
    salary = box.find("div",class_ = "srp-sal").get_text(strip = True)
    experience_required = box.find("div",class_ = "srp-exp").get_text(strip = True)
    location = box.find("div",class_ = "srp-loc").get_text(strip = True)
    job_link = box.find('h3').find('a')['href']
    
    job_data = {
        "title": title,
        "company_name": company_name,
        "posting_time": posting_time,
        "skills_required": skills_required,
        "salary": salary,
        "experience_required": experience_required,
        "location": location,
        "job_link": job_link,
    }
    return job_data
 


def prepare_soup(response_text):
    soup = BeautifulSoup(response_text, 'lxml')
    jobs_data = find_jobs_details(soup)
    display_web_results(jobs_data)
    return jobs_data

def Web_Scrapper(url):
    response = fetch_url_data(url)
    if check_status(response):
        prepare_soup(response.text)
    else:
        print("❌ Failed to access website.")

def display_web_results(jobs_list):
    for index, data in enumerate(jobs_list, start=1):
        print(f"\n🔹 Job {index}")
        print(f"📌 Title        : {data['title']}")
        print(f"🏢 Company Name : {data['company_name']}")
        print(f"🕒 Posted       : {data['posting_time']}")
        print(f"🧠 Skills       : {' | '.join(data['skills_required'])}")
        print(f"💰 Salary       : {(data['salary'])}")
        print(f"⏳ Experience Required       : {(data['experience_required'])}")
        print(f"📍 Location       : {(data['location'])}")
        print(f"🔗 Link       : {(data['job_link'])}")
        print("-" * 60)

def main():
    Web_Scrapper(WEB_URL)

if __name__ == "__main__":
    main()
