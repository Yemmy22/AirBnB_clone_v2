#!/usr/bin/python3

import os
from fabric.api import local, run
from datetime import datetime


def do_pack():
    '''
    do_pack function creates an archive
    from the contents of a directory
    '''
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "versions/web_static_{}.{}".format(time, "tgz")

    if not os.path.exists("versions"):
        local('mkdir versions')
        
    status = local('tar -cvzf {} web_static'.format(archive_name))
    if status.succeeded and os.path.exists(archive_name):
        return archive_name
    return None
