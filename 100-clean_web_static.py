#!/usr/bin/python3
# Fabfile to delete out-of-date archives.
import os
from fabric.api import *

env.hosts = ["104.196.168.90", "35.196.46.172"]


def do_clean(number=0):
    """Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """

    # convert number to int and set to 1 if 0
    number = 1 if int(number) == 0 else int(number)

    # sort archives and remove specified number
    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]

    # change local directory and remove archives
    with lcd("versions"):
    [local("rm ./{}".format(a)) for a in archives]

    # change remote directory and remove archives
    with cd("/data/web_static/releases"):
    # get list of archives and filter for web_static_
    archives = run("ls -tr").split()
    archives = [a for a in archives if "web_static_" in a]
    # remove specified number of archives
    [archives.pop() for i in range(number)]
    [run("rm -rf ./{}".format(a)) for a in archives]
