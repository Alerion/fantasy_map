import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools

    use_setuptools()

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(
    name='fantasy-map',
    version=__import__('map').__version__,
    description=__import__('map').__description__,
    long_description=README,
    license='The MIT License (MIT)',
    author='Dmitriy Kostochko',
    author_email='alerionum+django@gmail.com',
    packages=find_packages(exclude=['fantasy_map', 'fantasy_map.*']),
    url='https://github.com/Alerion/fantasy_map',
    keywords='Django, GIS',
    include_package_data=True,
    install_requires=['fake-factory'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
