#!/usr/bin/python3

"""Fab module - Static File archiving

Fabric script that generates a .tgz archive
from the contents of the web_static folder of your AirBnB Clone repo
using the function do_pack

Notes:
    * more info from: https://www.fabfile.org/
"""

from fabric.api import local, task
from datetime import datetime


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
    result = local(f'tar -cvf {archive_dir}/{archive_path} web_static/')
    return None if result.failed else result
