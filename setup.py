from distutils.core import setup
setup(name='freesscrawler',
    version='1.0.1',
    packages=['freess_crawler', 'freess_crawler.spiders'],
    package_data =  {'freess_crawler':['msgpacktool.so']},
    )
