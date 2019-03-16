import sys, re, pdb
from bs4 import BeautifulSoup as beautiful
from datetime import datetime
import requests

matching_titles = set()
missing_titles = set()
MATCH_ALL = r'.*'

def read_input_file():
    print('Reading input file')
    file = sys.argv[2]
    #?????
    return results

def get_zip_code():
    print(f'Got command line zip code {sys.argv[1]} ')
    return sys.argv[1]

def make_date_string():
    stamp = datetime.now()
    date_string = stamp.strftime('%Y-%d-%m-%H-%M-%S')
    return date_string

def make_time_string():
    stamp = datetime.now()
    time_string = stamp.strftime('%H:%M')
    return time_string



def build_site_url(template, title, zipcode='', radius='90', age='60'):
    """ Makes an url with each query item inserted into the url template
    site_id: type = str, value of site id like 'indeed' or 'careerbuilder'
    template: type = str, the url template.  example: 'http://indeed.com?{}&afg=&rfr=&title={}'
    title: type = str, job title using escape characters that are site dependent.  example: 'software+quality+engineer'
    zipcode: type = str, ZIP CODE
    radius: type = str, represents the radius of the job search. example: '50'  (miles)
    age: type = str, the number of days the job description has been posted.  example: '30' (days)

    returns an url string
    """
    url = template.format(title = title,  zipcode = zipcode, radius = radius, age = age)
    print(f'Built site url: {url}')
    return url


def build_job_title(title, title_separator):
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

def get_all_anchors(soup):
    print('Getting All Anchors')
    return soup('a')


def get_anchors_by_selector(title_selector, soup):
    print(f'Getting Anchors by selector: {title_selector}')
    return soup('a', title_selector)

def _add_site_id(site_id, ref):
    print('Adding site id to href for complete url')
    return f'http://{site_id}.com{ref}'


def _title_meets_threshold(title, title_word_values, threshold=90):
    print('Evaluating job title against threshold')
    total = 0
    if not title:
        return False
    t = re.sub(r"(?<=[A-z])\&(?=[A-z])", " ", title.lower())
    t = re.sub(r"(?<=[A-z])\-(?=[A-z])", " ", t)
    for word, value in title_word_values.items():
        if word.lower() in t:
            total+=value
    if total >= threshold:
        print(f'Met threshold: {title}')
        return True
    print(f'Not met threshold: {title}')
    return False

def get_soup(url):
    print(f'Getting raw html from: {url}' )
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'
    session = requests.Session()
    session.headers.update({'User-Agent': user_agent})
    response = session.get(url)
    body = response.text
    soup = beautiful(body, 'html.parser')
    print('Got raw html')
    return soup

def clean_text(text):
    return re.split(r'\W+', text)

def get_title_by_tag(selector, tag, soup):
    print(f'Getting job title by tag: {tag}, selector: {selector}')
    data = soup(tag, selector)
    text = ''
    if data:
        text = data[0].text
        text = text.strip('\n')
        text = text.strip()
    print(f'Got title: {text}')
    return text


def filter_links(links, link_selector):
    print(f'Filtering links, selector:{link_selector}')
    return [link for link in links if link_selector.lower() in link.lower()]


def like(string):
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







