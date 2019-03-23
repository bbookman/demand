from constants import SITES_DICT, SKILL_KEYWORDS, TITLES
from utility import *
import ssl, pdb
import pandas as pd
import matplotlib

ssl._create_default_https_context = ssl._create_unverified_context

if __name__ == '__main__':
    start = make_time_string()
    d = make_date_string()
    set_log(f'app_{d}.log', logging.DEBUG)   #todo make level a command line arg or setting in param file

    skills = [skill.lower() for skill in SKILL_KEYWORDS]
    job_skills = {}

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
            zipcode = get_zip_code()
            url = build_site_url(template, title, zipcode, radius='90', age='60')
            soup = get_soup(url)

            if anchor_method == 'selector':
                anchors = get_anchors_by_selector(link_selector, soup)
                titles = [anchor.get('title') for anchor in anchors]
                hrefs = [ref.get('href') for ref in anchors if ref.get('href') is not None]
            elif anchor_method == 'all':
                anchors = get_all_anchors(soup)
                if tag:
                    titles = list()
                    hrefs = [anchor.get('href') for anchor in anchors if anchor.get('href') is not None and link_selector in anchor.get('href')]
                    for ref in hrefs:
                        if prepend:
                            ref = add_site_id(site_id, ref)
                        data = get_soup(ref)
                        titles.append(get_title_by_tag(title_selector, tag, data))
                else:
                    titles = [anchor.text for anchor in anchors]
                    hrefs = [anchor.get('href') for anchor in anchors if anchor.get('href') is not None]

            ref_dict = dict(list(zip(titles, hrefs)))

            for title, ref in ref_dict.items():
                dups = set()
                if title_meets_threshold(title, title_word_values):
                    if prepend:
                        link =  add_site_id(site_id, ref) #REQUIRES APPENDING SITE ID
                    else:
                        link = ref
                    if link:
                        if link not in dups:
                            dups.add(link)
                            data = get_soup(link)
                            text = data.get_text()
                            ctext = clean_text(text)
                            hits = set()
                            for skill in skills:
                                job_skills.setdefault(skill, 0)
                                if skill not in hits:
                                    data = [word.lower() for word in ctext]
                                    if skill.lower() in data:
                                        print_and_log(f'Found: {skill}')
                                        hits.add(skill.lower())
                                        job_skills[skill.lower()] += 1
                        else:
                            print_and_log('Duplicate link - skipping', 'debug')
                    else:
                        print_and_log(f'{site_id}: invalid url: {ref}', 'debug')
    if not job_skills:
        try:
            raise ValueError('No skills found!!!!!')
        finally:
            print('Exiting')
    series = pd.Series(job_skills)
    series = pd.Series(job_skills)
    df = series.to_frame('skill_count')
    df.sort_values('skill_count', ascending=False, inplace=True)
    df['percent'] = df['skill_count'] / df['skill_count'].sum() * 100
    df2 = df[df.percent >= 3.0]
    print(df2)


    file_name = f'{original_title}_{zipcode}_results.txt'
    with open(file_name, 'w') as file:
        file.write(f'[{original_title}: [{zipcode}: {job_skills}  ]]')

    end = make_time_string()
    print_and_log(f'start: {start}, end: {end}', 'debug')
