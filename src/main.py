from constants import SITES_DICT, SKILL_KEYWORDS, TITLES
from utility import build_site_url, build_job_title, get_anchors_by_selector, _title_meets_threshold, clean_text, get_soup, make_time_string, _add_site_id, get_all_anchors, like, get_title_by_tag, filter_links
import ssl, pdb

ssl._create_default_https_context = ssl._create_unverified_context

if __name__ == '__main__':
    start = make_time_string()
    skills = [skill.lower() for skill in SKILL_KEYWORDS]
    job_skills = {}

    for site_id in SITES_DICT.keys():
        print(f'START: {site_id}')
        for original_title in TITLES.keys():
            anchor_method = SITES_DICT[site_id]['anchor_method']
            title_selector = SITES_DICT[site_id]['title_selector']
            tag = SITES_DICT[site_id]['title_tag']
            link_selector = SITES_DICT[site_id]['link_selector']
            title_word_values = TITLES[original_title][0]
            title_sep = SITES_DICT[site_id]['title_word_sep']
            title = build_job_title(original_title, title_sep)
            template = SITES_DICT[site_id]['url_template']
            zipcode = '95054' #todo
            url = build_site_url(template, title, zipcode, radius='90', age='60')
            soup = get_soup(url)


            if anchor_method == 'selector':
                anchors = get_anchors_by_selector(link_selector, soup)
                titles = [anchor.get('title') for anchor in anchors]
                hrefs = [ref.get('href') for ref in anchors if ref.get('href') is not None]
            elif anchor_method == ' all':
                anchors = get_all_anchors(soup)  #GET all anchors
                if site_id == 'careerbuilder': #GET TITLES FROM ANCHOR
                    titles = [anchor.text for anchor in anchors]
                    hrefs = [anchor.get('href') for anchor in anchors if anchor.get('href') is not None]
                if site_id == 'ziprecruiter':  #GET anchors by tag
                    titles = list()
                    hrefs = [anchor.get('href') for anchor in anchors if anchor.get('href') is not None and link_selector in anchor.get('href')]
                    for ref in hrefs:
                        data = get_soup(ref)
                        titles.append(get_title_by_tag(title_selector, tag, data))
            ref_dict = dict(list(zip(titles, hrefs)))

            for title, ref in ref_dict.items():
                if _title_meets_threshold(title, title_word_values):
                    if site_id == 'stackoverflow' or site_id == 'careerbuilder' or site_id == 'indeed':  #TODO SITES_DICT VARIABLE SHOULD DETERMINE THIS
                        link =  _add_site_id(site_id, ref) #REQUIRES APPENDING SITE ID
                    else:
                        link = ref
                    if link:
                        print(f'MET THRESHOLD: {title}, url:{link}')
                        data = get_soup(link)
                        text = data.get_text()
                        ctext = clean_text(text)
                        hits = set()
                        for skill in skills:
                            job_skills.setdefault(skill, 0)
                            if skill not in hits:
                                data = [word.lower() for word in ctext]
                                if skill.lower() in data:
                                        hits.add(skill.lower())
                                        job_skills[skill.lower()] += 1
                                        print(f'FOUND SKILL site: {site_id}, title:{title}, {skill}')
                    else:
                        print(f'{site_id}: invalid url: {ref}')

    print(job_skills)
    file_name = f'{original_title}_{zipcode}_results.txt'
    with open(file_name, 'w') as file:
        file.write(f'[{original_title}: [{zipcode}: {job_skills}  ]]')


    end = make_time_string()
    print(f'start: {start}, end: {end}')
    print(f'RESULTS: {file_name}')
