from constants import SITES_DICT, SKILL_KEYWORDS, TITLES
from utility import _build_site_url, _build_job_title, _get_jd_links_by_selector, _title_meets_threshold, _clean_text, _get_soup, _make_time_string, _add_site_id, _get_jd_links_by_brute_force, _get_titles_by_class
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

if __name__ == '__main__':
    start = _make_time_string()
    skills = [skill.lower() for skill in SKILL_KEYWORDS]
    job_skills = {}

    for site_id in SITES_DICT.keys():
        for original_title in TITLES.keys():
            title_selector = SITES_DICT[site_id]['title_selector']
            tag = SITES_DICT[site_id]['title_selector_tag']
            link_selector = SITES_DICT[site_id]['link_selector']
            title_word_values = TITLES[original_title][0]
            title_sep = SITES_DICT[site_id]['title_word_sep']
            title = _build_job_title(original_title, title_sep)
            template = SITES_DICT[site_id]['url_template']
            zipcode = '95054' #todo
            url = _build_site_url(site_id, template, title, zipcode, radius='90', age='60')
            print(f'site: {site_id}, title:{original_title}, url:{url}')
            soup = _get_soup(url)
            ids = ['stackoverflow', 'indeed', 'careerbulder']
            if site_id in ids:
                anchors = _get_jd_links_by_selector(link_selector, soup)
                titles = [anchor.get('title') for anchor in anchors]
                hrefs = [ref.get('href') for ref in anchors]
            elif site_id ==  'ziprecruiter':
                anchors = _get_jd_links_by_brute_force(soup)
                hrefs = [anchor.get('href') for anchor in anchors if anchor.get('href') is not None]
                titles = _get_titles_by_class(title_selector, tag, soup)
                import pdb; pdb.set_trace()
                print()
            ref_dict = dict(list(zip(titles, hrefs)))
            for title, ref in ref_dict.items():
                if _title_meets_threshold(title, title_word_values):
                    link =  _add_site_id(site_id, ref)
                    print(f'met threshold: {title}, url:{link}')
                    data = _get_soup(link)
                    text = data.get_text()
                    clean_text = _clean_text(text)
                    hits = set()
                    for skill in skills:
                        job_skills.setdefault(skill, 0)
                        if skill not in hits:
                            data = [word.lower() for word in clean_text]
                            if skill.lower() in data:
                                    hits.add(skill.lower())
                                    job_skills[skill.lower()] += 1
                                    print(f'site: {site_id}, title:{title}, {skill} found')
                else:
                    print(f'title:{title} does not meet threshold')
    print(job_skills)
    file_name = f'{title}_{zipcode}_results.txt'
    with open(file_name, 'w') as file:
        file.write(f'[{original_title}: [{zip}: {job_skills}  ]]')


    end = _make_time_string()
    print(f'start: {start}, end: {end}')
    print(f'RESULTS: {file_name}')
