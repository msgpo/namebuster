import setuptools

long_description = open('README.md', 'r').read()

requirements = list(open('requirements.txt', 'r'))

setuptools.setup(
    name='namebuster',
    version='1.0.0',
    scripts=['namebuster'] ,
    author='Ben Busby',
    author_email='contact@benbusby.com',
    install_requires=requirements,
    description='A tool for generating a list of username permutations from a list of names, a file, or url, to use for brute forcing',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/benbusby/namebuster',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
