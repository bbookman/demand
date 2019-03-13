import sys, re, pdb
from bs4 import BeautifulSoup as beautiful
from datetime import datetime
import requests

matching_titles = set()
missing_titles = set()
MATCH_ALL = r'.*'

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



def _build_site_url(template, title, zipcode='', radius='90', age='60'):
    """ Makes an url with each query item inserted into the url template
    site_id: type = str, value of site id like 'indeed' or 'careerbuilder'
    template: type = str, the url template.  example: 'http://indeed.com?{}&afg=&rfr=&title={}'
    title: type = str, job title using escape characters that are site dependent.  example: 'software+quality+engineer'
    zipcode: type = str, ZIP CODE
    radius: type = str, represents the radius of the job search. example: '50'  (miles)
    age: type = str, the number of days the job description has been posted.  example: '30' (days)

    returns an url string
    """

    return template.format(title = title,  zipcode = zipcode, radius = radius, age = age)


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

def _get_jd_links_by_anchor(soup):
    return soup('a')


def _get_jd_links_by_selector(title_selector, soup):
    return soup('a', title_selector)

def _add_site_id(site_id, ref):
    return f'http://{site_id}.com{ref}'


def _title_meets_threshold(title, title_word_values, threshold=90):
    total = 0
    if not title:
        return False
    t = re.sub(r"(?<=[A-z])\&(?=[A-z])", " ", title.lower())
    t = re.sub(r"(?<=[A-z])\-(?=[A-z])", " ", t)
    for word, value in title_word_values.items():
        if word.lower() in t:
            total+=value
    if total >= threshold:
        return True
    return False

def _get_soup(url):

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'
    session = requests.Session()
    session.headers.update({'User-Agent': user_agent})
    response = session.get(url)
    body = response.text
    soup = beautiful(body, 'html.parser')
    return soup

def _clean_text(text):
    return re.split(r'\W+', text)

def _get_titles_by_class(selector, tag, soup):
    title_objects = soup(tag, selector)
    return [title.text for title in title_objects]


def _filter_links(links, link_selector):
    return [link for link in links if link_selector.lower() in link.lower()]


def _like(string):
    """
    Return a compiled regular expression that matches the given
    string with any prefix and postfix, e.g. if string = "hello",
    the returned regex matches r".*hello.*"
    """
    string_ = string
    if not isinstance(string_, str):
        string_ = str(string_)
    regex = MATCH_ALL + re.escape(string_) + MATCH_ALL
    return re.compile(regex, flags=re.DOTALL)







