import sys, re, pdb
from bs4 import BeautifulSoup as beautiful
from datetime import datetime
import requests, logging
import timeout_decorator, pandas as pd
import socket, urllib3


def read_input_file():
    #todo - what if argument is not there or invalid?
    print_and_log('Reading input file')
    file = sys.argv[2]
    #?????
    return results

def get_zip_code():
    # First argument ..
    # todo what if arg is not there or invalid
    print_and_log(f'Got command line zip code {sys.argv[1]} ', 'info')
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
    print_and_log(f'Built site url: {url}')
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

@timeout_decorator.timeout(10)
def get_all_anchors(soup):
    print_and_log('Getting All Anchors')
    return soup('a')

@timeout_decorator.timeout(10)
def get_anchors_by_selector(title_selector, soup):
    print_and_log(f'Getting Anchors by selector: {title_selector}')
    return soup('a', title_selector)

def add_site_id(site_id, ref):
    print_and_log('Adding site id to href for complete url')
    return f'http://{site_id}.com{ref}'


def title_meets_threshold(title, title_word_values, threshold=90):
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
        print_and_log(f'Met threshold: {title}')
        return True
    print_and_log(f'Not met threshold: {title}')
    return False

@timeout_decorator.timeout(10)
def get_soup(url, skill_dict):
    soup = None
    if url == 'http://dice.com/jobs/browsejobs':

        print_and_log(make_data_frame(skill_dict))
        sys.exit()
    elif url in 'http://simplyhired.comhttps://www.simplyhired':
        return soup
    else:
        print_and_log(f'Getting raw html from: {url}' )
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'
        session = requests.Session()
        session.headers.update({'User-Agent': user_agent})
        try:
            response = session.get(url)
            body = response.text
            soup = beautiful(body, 'html.parser')
            print_and_log('Got raw html')
        except urllib3.exceptions.NewConnectionError as e:
            print_and_log(e, 'error')
            write_file(skill_dict, title='new_connection_error_encountered_captured_results')
        except socket.gaierror as s:
            print_and_log(s, 'error')
            write_file(skill_dict, title='socket_error_encountered_captured_results')
        except socket.error as e:
            print_and_log(e, 'error')
            write_file(skill_dict, title='socket_error_encountered_captured_results')
        except Exception as e:
            print_and_log(e, 'error')
            write_file(skill_dict, title='exception_encountered_captured_results')
        except BaseException as b:
            print_and_log(b, 'error')
            write_file(skill_dict, title='exception_encountered_captured_results')

        return soup


def clean_text(text):
    body = re.split(r'\W+', text)
    return [word.lower() for word in body]

@timeout_decorator.timeout(10)
def get_title_by_tag(selector, tag, soup):
    print_and_log(f'Getting job title by tag: {tag}, selector: {selector}')
    data = soup(tag, selector)
    text = ''
    if data:
        text = data[0].text
        text = text.strip('\n')
        text = text.strip()
        text = text.rstrip()
        text = text.lstrip()
    print_and_log(f'Got title: {text}')
    return text

@timeout_decorator.timeout(10)
def filter_links(links, link_selector):
    print_and_log(f'Filtering links, selector:{link_selector}')
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


def set_log(filename, level): #todo level options
    logging.basicConfig(filename=filename, level=level)


def report(e: Exception):
    logging.exception(str(e))

def print_and_log(text, level = 'info'):
    print(text)
    if level == 'debug':
        logging.debug(text)
    elif level == 'info':
        logging.info(text)
    elif level == 'warning':
        logging.warning(text)


def make_data_frame(skill_dict):
    series = pd.Series(skill_dict)
    df = series.to_frame('skill_count')
    df.sort_values('skill_count', ascending=False, inplace=True)
    df['percent'] = df['skill_count'] / df['skill_count'].sum() * 100
    df.round(2)
    return df

def write_file(skill_dict, zipcode = '99999', title = 'RESULTS', ):
    d = make_date_string()
    file_name = f'{title}_{zipcode}_{d}results.txt'
    with open(file_name, 'w') as file:
        file.write(f'[{title}: [{zipcode}: {skill_dict}  ]]')
