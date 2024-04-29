#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers

execute: fab -f 3-deploy_web_static.py deploy -i ~/.ssh/id_rsa -u ubuntu
"""

import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

env.hosts = ["54.85.131.209", "100.25.163.221"]


def do_pack():
    """
    Creates a tar.gz archive of the 'web_static' directory.

    Returns the path to the created archive if successful,
    or None if any step of the process fails.
    """

    # get current UTC time and format it as a string
    date = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    # construct the my_file my_file_name for the archive
    my_file = f"versions/web_static_{date}.tgz"

    # if the 'versions' directory doesn't exist, create it
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None

    # create the archive using tar
    # the '-cvzf' options tell tar to create an archive in gzip format
    if local("tar -cvzf {} web_static".format(my_file)).failed is True:
        return None

    # return the path to the created archive
    return my_file


def do_deploy(archive_path):
    """
    Deploys a tar.gz archive to the remote server.

    Args:
        archive_path (str): Path to the local archive my_file.

    Returns:
        bool: True if the deployment was successful, False otherwise.
    """

    # check if the archive my_file exists
    if os.path.isfile(archive_path) is False:
        return False

    # extract archive my_file my_file_name and release my_file_name
    my_file = archive_path.split("/")[-1]
    my_file_name = my_file.split(".")[0]
    original = f"/data/web_static/releases/{my_file_name}/"
    # upload the archive my_file to the remote server
    if put(archive_path, f"/ tmp/{my_file}").failed:
        return False

    # remove the release directory if it exists
    if run(f"rm -rf /data/web_static/releases/{my_file_name}").failed:
        return False

    # create the release directory
    if run(f"mkdir -p /data/web_static/releases/{my_file_name}").failed:
        return False

    # extract the archive to the release directory
    if run(f"tar -xzf /tmp/{my_file} -C {original}").failed:
        return False

    # remove the uploaded archive my_file
    if run(f"rm /tmp/{my_file}").failed:
        return False

    # move the contents of the extracted archive to the release directory
    if run(f"mv /data/web_static/releases/{my_file_name}/web_static/* "
           f"/data/web_static/releases/{my_file_name}/").failed:
        return False

    # remove the extracted directory
    if run(f"rm -rf {original}/web_static").failed:
        return False

    # remove the current symlink
    if run("rm -rf /data/web_static/current").failed:
        return False

    # create a symlink to the newly deployed release
    if run(f"ln -s {original} /data/web_static/current").failed:
        return False

    # deployment successful
    return True


def deploy():
    """
    Deploys the latest version of the web application.

    This function first packs the latest version of the application
    using the `do_pack` function. If the packing is successful,
    it then deploys the packed version using the `do_deploy` function.

    Returns:
        bool: True if the deployment was successful, False otherwise.
    """

    # pack the latest version of the web application
    packed_file = do_pack()

    # if packing was not successful, return False
    if packed_file is None:
        return False

    # deploy the packed version of the application
    deployment_status = do_deploy(packed_file)

    # return the status of the deployment
    return deployment_status
