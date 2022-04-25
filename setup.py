from setuptools import setup

setup(
    name='uposatha-ical',
    version='0.1.0',
    packages=['forest_sangha_moons'],
    url='https://github.com/jhanarato/uposatha-ical',
    license='MIT',
    author='Ajahn Jhanarato',
    author_email='jhanarato@gmail.com',
    description='Imports moon day information from icalendar',
    install_requires=[
        "icalendar >= 4.0.9"
    ]
)
