from setuptools import setup

setup(
    name='snmpdesk',
    version='0.0.1',
    description='Scripts for easy get snmp data',
    author='Svincov Dmitry',
    author_email='spam@19216801.ru',
    url='http://github.com/uralbash/snmpdesk/',
    py_modules=['snmpdesk'],
    install_requires=['pysnmp'],
    license='GPL',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: System :: Networking :: Monitoring',
        ],
)
