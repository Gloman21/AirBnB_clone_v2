#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive from the contents
of the web_static folder of your AirBnB Clone repo, using the function do_pack
"""
from fabric.api import *
from datetime import datetime

def pack():

    """
    making archive on web_static folder"""

    time = datetime.now
    timestamp = time.strftime("%Y%m%d%H%M%S")
    archive = 'web_static_' + timestamp + '.tgz'
    local('mkdir -p versions')
    create = local('tar -cvzf versions/{} web_static'.format(archive))
    if create is not None:
        return archive
    else:
        return None

