from setuptools import setup, Extension, find_packages



with open('README.md') as f:
	extd_desc = f.read()

with open('LICENSE') as f:
    license = f.read()

requirements_noversion = [
	'pandas',
    'sqlalchemy',
    'deg'
]
setup(
	# Meta information
	name				= 'diwier',
	version				= '0.1.0',
	author				= 'Supratik Chatterjee',
	author_email			= 'supratikdevm96@gmail.com',
	url				= 'https://github.com/supratikchatterjee16/diwier',
	description			= 'Search Engine Results Page Bot',
	keywords			= ['serp','bot', 'webscraping', 'scraping', 'search engine', 'package', 'python', 'crawler'],
	install_requires		= requirements_noversion,
	# build information
	py_modules			= ['diwier'],
	packages			= find_packages(),
	package_dir			= {'diwier' : 'diwier'},
	include_package_data		= True,
	long_description		= extd_desc,
	long_description_content_type	='text/markdown',
	# package_data			= {'diwier' : [
	# 					'databank/*',
	# 					'datadump/*',
	# 					'factuals/*'
	# 					]},

	zip_safe			= True,
	# https://stackoverflow.com/questions/14399534/reference-requirements-txt-for-the-install-requires-kwarg-in-setuptools-setup-py
	classifiers			= [
		"Programming Language :: Python :: 3",
		"Operating System :: OS Independent",
	],
	license 			= license
)