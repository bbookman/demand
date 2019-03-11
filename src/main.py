from utility import *

site_id = 'stackoverflow'
template = SITES_DICT['stackoverflow']['url_template']
zipcode = '95054'
url = _build_site_url(site_id, template, title, zipcode='', radius='90', age='60')
print(url)