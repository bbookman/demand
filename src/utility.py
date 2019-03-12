import sys, re
import urllib.request as urllib2
from bs4 import BeautifulSoup as beautiful
from datetime import datetime
import logging
from constants import *
import lxml
from lxml.html.clean import Cleaner

matching_titles = set()
missing_titles = set()

def _read_input_file():
    file = open(sys.argv[2], "r")
    results = file.read()
    file.close()
    return results

def _get_zip_code():
    return sys.argv[1]

def _make_date_string():
    stamp = datetime.now()
    date_string = stamp.strftime('%Y-%d-%m-%H-%M-%S')
    return date_string

def _make_time_string():
    stamp = datetime.now()
    time_string = stamp.strftime('%H:%M')
    return time_string



def _build_site_url(site_id, template, title, zipcode='', radius='90', age='60'):
    """ Makes an url with each query item inserted into the url template
    site_id: type = str, value of site id like 'indeed' or 'careerbuilder'
    template: type = str, the url template.  example: 'http://indeed.com?{}&afg=&rfr=&title={}'
    title: type = str, job title using escape characters that are site dependent.  example: 'software+quality+engineer'
    zipcode: type = str, ZIP CODE
    radius: type = str, represents the radius of the job search. example: '50'  (miles)
    age: type = str, the number of days the job description has been posted.  example: '30' (days)

    returns an url string
    """
    if site_id == 'indeed' or site_id =='ziprecruiter' or site_id == 'stackoverflow':
        return template.format(title = title,  zipcode = zipcode, radius = radius, age = age)
    if site_id == 'careerbuilder':
        cbtitle = _build_job_title(title, '-')
        title = _build_job_title(title, '+')
        return template.format(title = title, zipcode = zipcode, radius = radius, age = age, cbtitle = cbtitle)

def _build_job_title(title, title_separator):
    """ Takes list of title words and adds site specific separator between words
    title: string
    separator: type = string
    returns string
    """
    result =''
    words = title.split()
    for word in words:
        result+= word + title_separator
    return result[:-1]

def _get_job_description_links(title_selector, soup):
    return soup('a', title_selector)

def _add_site_id(site_id, hrefs):
    return [f'http://{site_id}.com{ref}' for ref in hrefs]


def _title_meets_threshold(title, title_word_values, threshold=90):
    total = 0
    if not title:
        return False
    t = re.sub(r"(?<=[A-z])\&(?=[A-z])", " ", title)
    t = re.sub(r"(?<=[A-z])\-(?=[A-z])", " ", t)
    for word, value in title_word_values.items():
        if word.lower() in t.lower():
            total+=value
    if total >= threshold:
        return True
    return False

def _get_soup(url):
    page = urllib2.urlopen(url)
    soup = beautiful(page, 'html.parser')
    return soup

def _clean_text(text):
    return re.split(r'\W+', text)




'''   TEMP   '''
result = dict()
geo = dict()
job_skills = dict()
skills = SKILL_KEYWORDS
site_id = 'stackoverflow'
original_title = 'data science engineer'
title_selector =  SITES_DICT[site_id]['title_selector']
title_word_values = TITLES[original_title][0]
title_sep = SITES_DICT[site_id]['title_word_sep']
title = _build_job_title(original_title, title_sep)

template = SITES_DICT['stackoverflow']['url_template']
zipcode = '95054'
url = _build_site_url(site_id , template, title, zipcode, radius='90', age='60')
soup = _get_soup(url)

anchors = _get_job_description_links(title_selector, soup)
titles = [anchor.get('title') for anchor in anchors]
hrefs = [ref.get('href') for ref in anchors]
ref_dict = dict(list(zip(titles, hrefs)))
filterd_links = list()
for title, value in ref_dict.items():
    if _title_meets_threshold(title, title_word_values):
        filterd_links.append(ref_dict[title])
links = [f'http://{site_id}.com' + link for link in filterd_links]
for link in links:
    data = _get_soup(link)
    text = data.get_text()
    clean_text = _clean_text(text)
    hits = set()
    for skill in skills:
        job_skills.setdefault(skill, 0)
        if skill in hits:
            break
        for word in clean_text:
            if word.lower() == skill.lower():
                hits.add(skill.lower())
                job_skills[skill]+=1












