import os

from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, sudo, put

import random

REPO_URL = 'git@github.com:erfanghoreishi/kanoodle-solver.git'


def deploy():
    _init_env()

    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'

    setting_path = "/home/erfan/Desktop/parsian/portal/portal/settings.py"

    _run_tests()
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    _run_server(source_folder)
    # _reload_celery_service()
    # _reload_gunicorn_service()


def _init_env():
    env.host = 'staging.parsiancrm.ir'
    env.host_string = 'ubuntu@188.121.100.222'
    env.user = 'ubuntu'


def _run_tests():
    run(f'./manage.py test')


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'venv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')

    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/kanoodle/settings.py'

    sed(settings_path,
        'db_password',
        'password@parsianeportal.ir')

    """
        command = f"sed s/\'password\'/'password@parsianeportal.ir'/ {settings_path}" \
                  f">/home/erfan/Desktop/parsian/portal/portal/setting.py"
        run(command)
    """


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../venv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')


def _update_static_files(source_folder):
    run(
        f'cd {source_folder}'
        ' && ../venv/bin/python3 manage.py collectstatic --noinput'
    )


def _update_database(source_folder):
    run(
        f'cd {source_folder}'
        ' && ../venv/bin/python3 manage.py migrate --noinput'
    )


def _run_server(source_folder):
    run(
        f'cd {source_folder}'
        ' && ../venv/bin/python3 manage.py runserver 0.0.0.0:8000'
    )


def _reload_gunicorn_service():
    sudo('systemctl stop gunicorn-superlists-staging.ottg.eu')
    sudo('systemctl start gunicorn-superlists-staging.ottg.eu')


def _reload_celery_service():
    sudo('systemctl stop celery-portal-staging.parsiancrm.ir.service')
    sudo('systemctl start celery-portal-staging.parsiancrm.ir.service')


def _reload_celery_heartbeat_service():
    sudo('systemctl stop celery-beat-portal-staging.parsiancrm.ir.service')
    sudo('systemctl start celery-beat-portal-staging.parsiancrm.ir.service')
