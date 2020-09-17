from distutils.core import setup
from setuptools import find_packages


setup(
    name='drkns',
    version='0.0.2',
    packages=find_packages('./'),
    package_dir={'./src': 'src'},
    url='',
    license='MIT',
    author='Fräntz Miccoli',
    description='',
    scripts=['../bin/drkns'],
    install_requires=[
        'awscli>=1,<2',
        'dirhash>=0.2,<1.0',
        'PyYAML>=5.3,<6.0'
    ],
)
