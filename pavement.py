from paver.easy import sh, task
import os


@task
def build():
    if os.path.exists('./build'):
        sh('rm -rf ./build')

    build_script = '''
        mkdir ./build
        cp -rf ./src/* ./build/
        (cd ./build; python setup.py sdist bdist_wheel)
    '''

    sh(build_script)
