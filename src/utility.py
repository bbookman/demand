import sys
import urllib.request as urllib2
from bs4 import BeautifulSoup as beautiful
from datetime import datetime
import logging
from constants import *

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

def _start_driver():
    """ Starts the chrome webdriver in headless mode """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('window-size=1920x1080')
    try:
        driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)
    except SessionNotCreatedException as e:
        print('SessionNotCreatedException - try again')
        logging.debug(e)
        try:
            driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)
        except SessionNotCreatedException as s:
            print('Terminating')
            logging.debug(s)
    return driver



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

def _get_job_description_links(title_selector, url):
    page = urllib2.urlopen(url)
    soup = beautiful(page, 'html.parser')
    links = soup(title_selector)
    return [str(link) for link in links]


'''   TEMP   '''


site_id = 'stackoverflow'
title_sep = SITES_DICT[site_id]['title_word_sep']
title = _build_job_title('data science engineer', title_sep)

template = SITES_DICT['stackoverflow']['url_template']
zipcode = '95054'
url = _build_site_url(site_id, template, title, zipcode, radius='90', age='60')
