import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='snmpdesk',
    version='0.0.7',
    description='Scripts for easy get snmp data',
    author='Svintsov Dmitry',
    author_email='spam@19216801.ru',
    url='http://github.com/uralbash/snmpdesk/',
    keywords = "snmp",
    install_requires=['pysnmp'],
    license='GPL',
    packages=['snmpdesk'],
    long_description=read('README'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: System :: Networking :: Monitoring',
        ],
)
