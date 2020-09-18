from paver.easy import sh, task
import os


@task
def build():
    if os.path.exists('./build'):
        sh('rm -rf ./build')

    script = '''
        mkdir ./build
        cp -rf ./src/* ./build/
        (cd ./build; python setup.py sdist bdist_wheel)
    '''

    sh(script)


@task
def deploy():
    script = '''
        twine upload ./build/dist/*
    '''

    sh(script)
