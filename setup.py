from distutils.core import setup

setup(
    name='XSLClearer',
    version='0.1.3',
    author='Frédéric BISSON',
    author_email='zigazou@free.fr',
    packages=['xsls', 'xsls/keywords'],
    scripts=['bin/xslclearer','bin/xslsproc'],
    url='http://pypi.python.org/pypi/XSLClearer/',
    license='COPYING',
    description='XSLClearer makes writing XSL template easier to write.',
    long_description=open('README.txt').read(),
    install_requires=[
        "cssselect >= 0.9.1",
    ],
)
