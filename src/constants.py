SKILL_KEYWORDS =['python', 'c++', 'java', 'bash','ruby',
'perl', 'matlab', 'javascript', 'scala', 'firmware', 'Machine', ' Espresso', 'learning', 'map', 'reduce', 'big','ec2', 'warehouse', 'statistical', 'visualizations', 'visualization',
                 'php', 'Sauce Labs', 'flask', 'shell', 'solaris', 'Telecom', 'NAS', 'iSCSI', 'scripts', 'scripting','etl', 'collibra', 'onedata',
                 'junit', 'selenium', 'react', 'c#', 'TestRail', 'Confluence', 'JMeter', 'Vertica', 'Logstash', 'Kibana',
                'tableau', 'd3.js', 'sas', 'spss', 'd3', 'saas', 'pandas', 'numpy', 'Jenkins', 'scipy', 'plan', 'case',
                'sps', 'spotfire', 'scikits.learn', 'splunk', 'h2o', 'jira', 'functional', 'integration', 'stress', 'load','performance',
                'hadoop', 'mapreduce', 'spark', 'pig', 'hive', 'shark', 'oozie', 'zookeeper', 'flume', 'mahout', 'bi'
                'elasticsearch', 'api', 'apis', 'Mockito', 'Robotium', 'frontend', 'backend', 'Informatica', 'Julia',
              'sql', 'nosql', 'hbase', 'cassandra', 'xml', 'rust', 'mongodb', 'mysql', 'mssql', 'postgre', 'oracle',
             'rdbms', 'mobile', 'android', 'ios', 'cucumber', 'iot', 'black', 'white', 'telecommunications', 'Superset', 'ggplot',
             'hive', 'cucumber', 'aws', 'azure', 'amazon', 'google', 'rest', 'docker', 'container', 'puppet', 'chef',
             'kubernetes', 'storage', 'network', 'networking', 'maven', 'ci', 'cd', 'ci/cd', 'gui', 'marketing', 'MDM', 'PL/SQL',
            'restassured', 'ios', 'json', 'swift', 'objective-c', 'groovy', '.net', 'angular', 'node.js', 'kafka', 'mesos','go',
            'django', 'pytest', 'css', 'html', 'appium', 'linux', 'css', 'ui', 'soa', 'unix', 'RESTful', 'Elastic', 'git',
            'github', 'database', 'acceptance', 'uat', 'healthcare', 'banking', 'Excel', 'r', 'Statistics', 'Mathematics','SparkSQL',
            'druid', 'solr','economics', 'clickstream', 'haskell', 'nomad', 'nix', 'bazil', 'buck', 'key-value','NLP', 'Bayesian', 'Gurobi',
            'windows', 'C/C++', 'NVMe', 'SSD', 'HDD','Typescript','DNN','cnn', 'rnn', 'phd', 'mining', 'sem', 'audio', 'video']


SITES_DICT = {

    'careerbuilder': {
        'url_template': 'https://www.careerbuilder.com/jobs?keywords={title}&location={zipcode}&radius={radius}&posted={age}',
        'link_selector': 'siteid',
        'title_word_sep': '+',
        'title_class': '',
        'title_selector_tag': '',
    },

}


TITLES = {
    #'software quality assurance engineer': [{'software': 50, 'quality': 60, 'assurance': 30, 'qa': 80, 'sqa': 90, 'sdet': 100, 'test': 50, 'automation': 30, 'automated': 30, 'engineer': 20, 'testing': 70},
     #SKILL_KEYWORDS, True],
    'data science engineer': [{'data':60, 'science':30, 'engineer':30, 'engineering': 30, 'scientist': 30, 'quantitative': 50, 'analyst':40}, SKILL_KEYWORDS, False],
}

'''
        'stackoverflow': {
            'url_template': 'https://stackoverflow.com/jobs?q={title}&l={zipcode}&d={radius}&u=Miles&',
            'link_selector': 's-link',
            'title_word_sep': '+',
             'title_class': '',
             'title_selector_tag': '',
        },
      
        'ziprecruiter': {
        'url_template': 'http://www.ziprecruiter.com/candidate/search?search={title}&location={zipcode}&days={age}&radius={radius}&',
        'link_selector': 'clk',
        'title_word_sep': '+',
        'title_class': 'just_job_title',
        'title_selector_tag': 'span',

        },


        'careerbuilder': {
            'url_template': 'https://www.careerbuilder.com/jobs?location={zipcode}&radius={radius}&posted={age}',
            'link_selector': 'data-gtm="jrp-job-list|job-title-click|1"',
            'title_word_sep': '+',
            'title_class': '',
            'title_selector_tag': '',
        },

        'indeed': {
            'url_template': 'https://www.indeed.com/jobs?as_and={title}&radius={radius}&l={zipcode}&fromage={age}&limit=500&sort=&psf=advsrch',
            'link_selector': 'turnstileLink',
            'title_word_sep': '+',
             'title_class': '',
            'title_selector_tag': '',
        },
<a data-gtm="jrp-job-list|job-title-click|1" data-job-did="J3Q1ZS6HDCXKK0JH908" data-company-did="CD888N672X35PM4B3L0" href="/job/J3Q1ZS6HDCXKK0JH908?ipath=JRG1&amp;keywords=data+science+engineer&amp;location=95054&amp;searchid=dbcac81f-dc68-41c5-87ca-0c7a57184c3b%3AAPAb7IRe2bg9Z3HKTRTKa2aPtWQoWTSK5A%3D%3D&amp;siteid=cbnsv">Data Scientist</a>


'''