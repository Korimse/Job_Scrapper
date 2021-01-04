import requests
from bs4 import BeautifulSoup

JOBPLANET_URL = "https://www.jobplanet.co.kr/job_postings/search?utf8=%E2%9C%93&posting_type=&jp_min_salary=&jp_min_recommend=&recruitment_type_ids%5B%5D=1&occupation_level2_ids%5B%5D=11613&occupation_level2_ids%5B%5D=11606&occupation_level2_ids%5B%5D=11610&occupation_level2_ids%5B%5D=11607&occupation_level2_ids%5B%5D=11603&occupation_level2_ids%5B%5D=11604&order_by=score"

def get_last_pages():
  jobplanet_result = requests.get(JOBPLANET_URL)
  jobplanet_soup = BeautifulSoup(jobplanet_result.text, "html.parser")
  pagination = jobplanet_soup.find("article", {"class":"paginnation_new"})

  pages = []
  pages.append(int(pagination.find("strong", {"class":"txtlink_page"}).string))

  page_a = pagination.find_all('a')
  for page in page_a[:-2]:
    pages.append(int(page.string))

  max_page = pages[-1]
  return max_page

def extract_job(html, htmll, htmlll):
  title = html.find("a", {"class":"posting_name"}).string
  company = htmll.find("button", {"class":"btn_open"}).string
  location = htmlll.find("span", {"class":"tags"}).string
  return {'title':title, 'company':company, 'tags':location}


def extract_jobs(last_pages):
  jobs = []
  for page in range(last_pages):
    print(f"Scrapping page {page}")
    result = requests.get(f"{JOBPLANET_URL}&page={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")
    results_title = soup.find_all("div", {"class":"unit_head"})
    results_company = soup.find_all("div", {"class":"jp_data_builtin"})
    results_location = soup.find_all("div", {"class":"ui_fold_comp closed"})
    for result_title, result_company, result_location  in zip(results_title, results_company, results_location):
      job = extract_job(result_title, result_company, result_location)
      jobs.append(job)
  return jobs

def get_jobs():
  last_page = get_last_pages()
  jobs = extract_jobs(last_page)
  return jobs