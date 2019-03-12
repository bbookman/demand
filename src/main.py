from constants import SITES_DICT, SKILL_KEYWORDS, TITLES
from utility import _build_site_url, _build_job_title, _get_job_description_links, _title_meets_threshold, _clean_text, _get_soup, _make_time_string
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

if __name__ == '__main__':
    start = _make_time_string()

    result = dict()
    geo = dict()
    job_skills = dict()
    skills = SKILL_KEYWORDS


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
            print(f'url:{url}')
            soup = _get_soup(url)
            anchors = _get_job_description_links(title_selector, soup)
            titles = [anchor.get('title') for anchor in anchors]
            hrefs = [ref.get('href') for ref in anchors]
            ref_dict = dict(list(zip(titles, hrefs)))
            filterd_links = list()
            for title, value in ref_dict.items():
                if _title_meets_threshold(title, title_word_values):
                    filterd_links.append(ref_dict[title])
                    print(f'met threshold: {title}')
            links = [f'http://{site_id}.com' + link for link in filterd_links]
            for link in links:
                data = _get_soup(link)
                text = data.get_text()
                clean_text = _clean_text(text)
                hits = set()
                for skill in skills:
                    job_skills.setdefault(skill, 0)
                    if skill in hits:
                        break
                    for word in clean_text:
                        if skill in hits:
                            break
                        if word.lower() == skill.lower():
                            hits.add(skill.lower())
                            job_skills[skill] += 1
                            print(f'title:{original_title}, {skill} found')
print(job_skills)
end = _make_time_string()
print(f'start: {start}, end: {end}')
