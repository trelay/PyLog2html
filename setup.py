from distutils.core import setup
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
	long_description = f.read()

setup(name='PyLog2html',
	version='1.0.4',
	description='Python logging to html',
	long_description=long_description,
	author='Trelay Wang',
	author_email='trelwan@celestica.com',
	url='https://github.com/trelay/PyLog2html',
	license='MIT',
	classifiers=[
		# How mature is this project? Common values are
		#   3 - Alpha
		#   4 - Beta
		#   5 - Production/Stable
		'Development Status :: 5 - Production/Stable',

		# Indicate who your project is intended for
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',

		# Pick your license as you wish (should match "license" above)
		'License :: OSI Approved :: MIT License',

		# Specify the Python versions you support here. In particular, ensure
		# that you indicate whether you support Python 2, Python 3 or both.
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
    ],
	keywords='logging html',
	#packages=['PyLog2html'],
	py_modules=['HTMLLogger'],
	download_url='https://github.com/trelay/PyLog2html/tarball/1.0.4',
)
