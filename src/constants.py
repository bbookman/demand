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
        'stackoverflow': {
            'url_template': 'https://stackoverflow.com/jobs?q={title}&l={zipcode}&d={radius}&u=Miles&',
            'title_selector': 's-link',
            'title_word_sep': '+',
        },

}


TITLES = {
    #'software quality assurance engineer': [{'software': 50, 'quality': 60, 'assurance': 30, 'qa': 80, 'sqa': 90, 'sdet': 100, 'test': 50, 'automation': 30, 'automated': 30, 'engineer': 20, 'testing': 70},
     #SKILL_KEYWORDS, True],
    'data science engineer': [{'data':60, 'science':30, 'engineer':30, 'engineering': 30, 'scientist': 30, 'quantitative': 50, 'analyst':40}, SKILL_KEYWORDS, False],
}

'''
        'ziprecruiter': {
            'url_template': 'http://www.ziprecruiter.com/candidate/search?search={title}&location={zipcode}&days={age}&radius={radius}&',
            'title_selector': 'job_link',
            'title_word_sep': '+',

        },

        'careerbuilder': {
            'url_template': 'https://www.careerbuilder.com/jobs-{cbtitle}-in-{zipcode}?keywords={title}&location={zipcode}&radius={radius}&posted={age}&',
            'title_selector': "//h2[@class='job-title show-for-medium-up']//a[@data-gtm='jrp-job-list|job-title-click|{}']",
            'title_word_sep': '+',
        },

        'indeed': {
            'url_template': 'https://www.indeed.com/jobs?as_and={title}&radius={radius}&l={zipcode}&fromage={age}&limit=500&sort=&psf=advsrch',
            'title_selector': 'turnstileLink',
            'title_word_sep': '+',
        },


'''