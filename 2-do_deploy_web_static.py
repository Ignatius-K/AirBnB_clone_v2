#!/usr/bin/python3

"""Fab module - Static File deploying

Fabric script that generates a .tgz archive
and deploys it

Notes:
    * more info from: https://www.fabfile.org/
"""

from fabric.api import local, parallel, put, run, sudo, task, env
from datetime import datetime
import os

env.hosts = [
    '54.152.221.218',
    # '54.146.70.187'
]


@task
def do_pack():
    """generates a .tgz archive

    All files in the folder web_static must be added to the final archive
    All archives must be stored in the folder versions

    name of the archive created must be
    web_static_<year><month><day><hour><minute><second>.tgz

    Returns:
        str | None: The archive path
    """

    archive_dir = "versions/"
    result = local(f"mkdir -p {archive_dir}")
    if result.failed:
        return None
    archive_path = f'web_static_{datetime.now().strftime("%Y%m%d%H%M%S")}.tgz'
    result = local(f'tar -cvzf {archive_dir}/{archive_path} web_static/')
    return None if result.failed else result

@task
@parallel
def do_deploy(archive_path):
    """Delpoy archive to the specified hosts

    Args:
        archive_path (str): The path to archive

    Returns:
        bool: True if success
    """

    if not os.path.exists(archive_path):
        print('Archive file does not exist')
        return False

    # Upload archive
    upload_dir = '/tmp'
    filename = archive_path.split("/")[-1]
    uploaded_file = f'{upload_dir}/{filename}'
    result = put(archive_path, uploaded_file, use_sudo=True)
    if result.failed:
        print("Upload archive failed")
        return None

    # Uncompress archive
    uploaded_code = f'/data/web_static/releases/{filename.split(".")[0]}'
    result = sudo(f'mkdir -p {uploaded_code} && '+
                 f'tar --strip-components=1 -xvzf {result[0]} -C {uploaded_code}'
                )
    if result.failed:
        print('Uncompressing archive on remote failed')
        return None
    run(f'rm {uploaded_file}')

    # deploy
    app_sys_link = '/data/web_static/current'
    sudo(f'unlink {app_sys_link}', warn_only=True)
    result = sudo(f'ln -s {uploaded_code} {app_sys_link}')
    if result.failed:
        print('Failed to deploy')
        return False
    print('Deploy successful')
    return True
