from distutils.core import setup
from setuptools import find_packages

with open('../README.md') as readme_file:
    long_description = readme_file.read()

setup(
    name='drkns',
    version='1.3.1',
    description='Simple monorepo build tool',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/frantzmiccoli/drkns',
    packages=find_packages('./'),
    package_dir={'./src': 'src'},
    license='MIT',
    scripts=['../bin/drkns'],
    install_requires=[
        'awscli>=1,<2',
        'dirhash>=0.2,<1.0',
        'PyYAML>=5.3,<6.0'
    ],
    keywords="devops build test monorepo cache",
)
