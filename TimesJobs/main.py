from bs4 import BeautifulSoup as bs
import requests

#Sometimes not including the header results in a failed response
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Referer': 'https://cssspritegenerator.com',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.8'}

# The URL pertains to search results in Bengaluru. We may change the URL's going forward
BASE_URL = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=machine+learning+engineer&txtLocation=Bengaluru%2F+Bangalore'

html_text = requests.get(BASE_URL, headers=hdr)
soup = bs(html_text.content, 'html.parser')

# Start with getting the number of jobs found
header = soup.find('header', attrs={'class': 'srp-header clearfix'})
job_count = header.find('span', attrs={'id':'totolResultCountsClosingId'}).text
print(f'Number of jobs found: {job_count}')

# Get the jobs
jobs = soup.find_all('li', attrs={'class':'clearfix job-bx wht-shd-bx'})

# Create a list of dictionaries for storing jobs
jobs_list = []

for job in jobs:
    # We want to scrape data only for jobs that were 'Posted few days ago'
    post_date = job.find('span', attrs={'class':'sim-posted'}).text

    if 'few' in post_date:

        company_name = job.find('h3', attrs={'class':'joblist-comp-name'}).text.replace(' ', '')
        skills = job.find('span', attrs={'class':'srp-skills'}).text.replace(' ', '')
        required_exp = job.find('ul', attrs={'class':'top-jd-dtl clearfix'}).li.text.replace('card_travel', '')

        #print(f'Company Name: {company_name}')
        #print(f'Required Skills: {skills}')
        #print(f'Required Experience: {required_exp}')

        d_job = {'Company':company_name, 'Skills':skills, 'Experience':required_exp}
        jobs_list.append(d_job)
        
        #print('')
    print(jobs_list)