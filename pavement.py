from paver.easy import sh, task
import os


@task
def build():
    if os.path.exists('./dist'):
        sh('rm -rf ./dist')

    sh('uv build')


@task
def deploy():
    sh('twine upload ./dist/*')
