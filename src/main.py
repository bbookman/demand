from constants import SITES_DICT, SKILL_KEYWORDS, TITLES
from utility import _build_site_url, _build_job_title, _get_job_description_links, _title_meets_threshold, _clean_text, _get_soup, _make_time_string, _add_site_id
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

if __name__ == '__main__':
    start = _make_time_string()

    result = dict()
    geo = dict()
    job_skills = dict()
    skills = [skill.lower() for skill in SKILL_KEYWORDS]


    for site_id in SITES_DICT.keys():
        for original_title in TITLES.keys():
            print(f'site: {site_id}, title:{original_title}')
            title_selector = SITES_DICT[site_id]['title_selector']
            title_word_values = TITLES[original_title][0]
            title_sep = SITES_DICT[site_id]['title_word_sep']
            title = _build_job_title(original_title, title_sep)
            template = SITES_DICT[site_id]['url_template']
            zipcode = '95054' #todo
            url = _build_site_url(site_id, template, title, zipcode, radius='90', age='60')
            print(f'site: {site_id}, title:{original_title}, url:{url}')
            soup = _get_soup(url)
            anchors = _get_job_description_links(title_selector, soup)
            titles = [anchor.get('title') for anchor in anchors]
            hrefs = [ref.get('href') for ref in anchors]
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
end = _make_time_string()
print(f'start: {start}, end: {end}')
