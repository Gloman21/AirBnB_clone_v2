#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import local, run, put
from os.path import exists

env.hosts = ['54.89.109.87', '100.25.190.21']
env.user = "ubuntu"

def do_pack():
    """
    Packs the "web_static" directory into a .tgz archive and returns the
    path of the created archive. If the packing process fails, returns None.
    """

    # Create the "versions" directory if it doesn't exist
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None

    # Get the current date and time and format it as a string
    date = datetime.now().strftime("%Y%m%d%H%M%S")

    # Construct the path for the archive my_file
    arch_my_file_path = f"versions/web_static_{date}.tgz"

    # Pack the "web_static" directory into a .tgz archive and save it to the
    # specified path
    t_gzip = local(f"tar -cvzf {arch_my_file_path} web_static")

    # If the packing process succeeded, return the path of the created
    # archive, otherwise return None
    if t_gzip.succeeded:
        return arch_my_file_path
    else:
        return None


def do_deploy(archive_path):
    """
    Deploys a tar.gz archive to the remote server.

    Args:
        archive_path (str): Path to the local archive my_file.

    Returns:
        bool: True if the deployment was successful, False otherwise.
    """

    # Check if the archive my_file exists
    if os.path.isfile(archive_path) is False:
        return False

    # Extract archive my_file my_file_name and release my_file_name
    my_file = archive_path.split("/")[-1]
    my_file_name = my_file.split(".")[0]
    original = f"/data/web_static/releases/{my_file_name}/"

    # Upload the archive my_file to the remote server
    if put(archive_path, f"/ tmp/{my_file}").failed:
        return False

    # Remove the release directory if it exists
    if run(f"rm -rf /data/web_static/releases/{my_file_name}").failed:
        return False

    # Create the release directory
    if run(f"mkdir -p /data/web_static/releases/{my_file_name}").failed:
        return False

    # Extract the archive to the release directory
    if run(f"tar -xzf /tmp/{my_file} -C {original}").failed:
        return False

    # Remove the uploaded archive my_file
    if run(f"rm /tmp/{my_file}").failed:
        return False

    # Move the contents of the extracted archive to the release directory
    if run(f"mv /data/web_static/releases/{my_file_name}/web_static/* "
           f"/data/web_static/releases/{my_file_name}/").failed:
        return False

    # Remove the extracted directory
    if run(f"rm -rf {original}/web_static").failed:
        return False

    # Remove the current symlink
    if run("rm -rf /data/web_static/current").failed:
        return False

    # Create a symlink to the newly deployed release
    if run(f"ln -s {original} /data/web_static/current").failed:
        return False

    # Deployment successful
    return True
