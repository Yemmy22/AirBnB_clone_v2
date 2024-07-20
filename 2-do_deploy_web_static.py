#!/usr/bin/python3

import os
from fabric.api import local, run, env, put

env.user = 'ubuntu'
env.hosts = ['100.26.138.201', '54.209.126.230']
env.key_filename = "~/.ssh/id_rsa"


def do_deploy(archive_path):
    '''
    Deploys to two servers using command line parameters
    '''

    # Returns False if the file at the path archive_path doesn’t exist
    if not os.path.exists(archive_path):
        return False

    time_stamp = archive_path[-18:-4]

    try:
        # Upload archive to the /tmp/ directory of remote
        put(archive_path, '/tmp/')

        # Create a new directory with the archive name in the
        # /data/web_static/releases
        run('mkdir -p  /data/web_static/releases/web_static_{}'.format(time_stamp))

        # Uncompress the archive into the newly created directory
        run('tar -xzf /tmp/web_static_{}.tgz -C /data/web_static/releases/web_static_{}/'.format(time_stamp, time_stamp))

        # Deletes the archive from the tmp directory
        run('rm /tmp/web_static_{}.tgz'.format(time_stamp))

        # Move the content of the uncompressed archive
        # into its grand-parent directory
        run('rsync -aI /data/web_static/releases/web_static_{}/web_static/* /data/web_static/releases/web_static_{}/'.format(time_stamp, time_stamp))

        # Delete the empty archive directory
        run('rm -rf /data/web_static/releases/web_static_{}/web_static'.format(time_stamp))

        # Deletes the symbolic link /data/web_static/current
        # from the web server
        run('rm -rf /data/web_static/current')

        # Recreates a new the symbolic link
        run('ln -s /data/web_static/releases/web_static_{}/ /data/web_static/current'.format(time_stamp))

        # Reload the server
        run('sudo service nginx restart')

    except Exception as e:
        return False

    print('New version deployed!')
    return True
