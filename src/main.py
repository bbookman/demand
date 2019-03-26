from constants import SITES_DICT, SKILL_KEYWORDS, TITLES, SKILL_PHRASES
from utility import *
import ssl, pdb
#import matplotlib

ssl._create_default_https_context = ssl._create_unverified_context

if __name__ == '__main__':
    start = make_time_string()
    d = make_date_string()
    set_log(f'app_{d}.log', logging.DEBUG)   #todo make level a command line arg or setting in param file
    zipcode = get_zip_code()

    phrases = [p.lower() for p in SKILL_PHRASES]
    skills = [skill.lower() for skill in SKILL_KEYWORDS]
    job_skills = {}
    original_title = str()
    for skill in skills:
        job_skills.setdefault(skill, 0)
    for phrase in phrases:
        job_skills.setdefault(phrase, 0)

    for site_id in SITES_DICT.keys():
        print_and_log(f'START: {site_id}', 'debug')
        for original_title in TITLES.keys():
            anchor_method = SITES_DICT[site_id]['anchor_method']
            title_selector = SITES_DICT[site_id]['title_selector']
            tag = SITES_DICT[site_id]['title_tag']
            link_selector = SITES_DICT[site_id]['link_selector']
            title_word_values = TITLES[original_title][0]
            title_sep = SITES_DICT[site_id]['title_word_sep']
            title = build_job_title(original_title, title_sep)
            template = SITES_DICT[site_id]['url_template']
            prepend = SITES_DICT[site_id]['prepend_site_id']
            paging = SITES_DICT[site_id]['paging']
            urls = list()
            soups = list()
            hrefs = list()
            titles = list()
            if paging:
                for page in range(5):
                    url = (build_site_url(template, title, zipcode, radius='90', age='60'))
                    url = url + str(page)
                    urls.append(url)
            else:
                urls.append(build_site_url(template, title, zipcode, radius='90', age='60'))

            for url in urls:
                soups.append(get_soup(url, job_skills))

            for soup in soups:
                if anchor_method == 'selector' and soup:
                    anchors = get_anchors_by_selector(link_selector, soup)
                    titles = [anchor.get('title') for anchor in anchors]
                    hrefs = [ref.get('href') for ref in anchors if ref.get('href') is not None]

                elif anchor_method == 'all' and soup:
                    anchors = get_all_anchors(soup)
                    if tag:
                        titles = list()
                        hrefs = [anchor.get('href') for anchor in anchors if anchor.get('href') is not None and link_selector in anchor.get('href')]
                        for ref in hrefs:
                            if prepend:
                                ref = add_site_id(site_id, ref)
                            data = get_soup(ref, job_skills)
                            if not data:
                                print_and_log(f'Could not get soup from: {ref}')
                            titles.append(get_title_by_tag(title_selector, tag, data))
                    else:
                        titles = [anchor.text for anchor in anchors]
                        hrefs = [anchor.get('href') for anchor in anchors if anchor.get('href') is not None]

            ref_dict = dict(list(zip(titles, hrefs)))

            for title, ref in ref_dict.items():
                dups = set()
                if title_meets_threshold(title, title_word_values):
                    if prepend:
                        link = add_site_id(site_id, ref)
                    else:
                        link = ref
                    if link:
                        if link not in dups:
                            dups.add(link)
                            data = get_soup(link, job_skills)
                            if data:
                                text = data.get_text()
                                ctext = clean_text(text)
                                words = [word.lower() for word in ctext]
                                hits = set()
                                founds = set()
                                for phrase in phrases:
                                    if phrase.lower() not in hits:
                                        if phrase.lower() in ctext:
                                            hits.add(phrase.lower())
                                            job_skills[phrase.lower()] += 1
                                            print_and_log(f'Found: {phrase.lower()}')

                                for skill in skills:
                                    for word in words:
                                        if skill.lower() == word.lower() and skill not in founds:
                                            founds.add(skill.lower())
                                            job_skills[skill.lower()] += 1

                            else:
                                print_and_log(f'Could not get soup from: {link}')

                        else:
                            print_and_log('Duplicate link - skipping', 'debug')
                    else:
                        print_and_log(f'{site_id}: invalid url: {ref}', 'debug')
    if not job_skills:
        try:
            raise ValueError('No skills found!!!!!')
        finally:
            print('Exiting')
    df = make_data_frame(job_skills)
    df.round({'percent':2})
    print(df)
    with open('dataFrame.txt' 'w') as file:
        file.write(df)

    write_file(job_skills, title=original_title, zipcode=zipcode)

    end = make_time_string()
    print_and_log(f'start: {start}, end: {end}', 'debug')
