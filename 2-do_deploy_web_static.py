#!/usr/bin/python3

import os
from fabric.api import local, run, env, put

env.hosts = ['100.26.138.201', '54.209.126.230']
env.key_filename = "~/.ssh/id_rsa"
file_name = "web_static"


def do_deploy(archive_path):
    '''
    Deploys to two servers using command line parameters
    '''

    # Returns False if the file at the path archive_path doesn’t exist
    if not os.path.exists(f"{archive_path}"):
        return False

    parent_dir, archive_name = f"{archive_path}".split('/')
    archive_dir, ext = f"{archive_name}".split('.')

    try:
        # Upload archive to the /tmp/ directory of remote
        put(archive_path, '/tmp/')

        # Create a new directory with the archive name in the
        # /data/web_static/releases
        run(f"mkdir -p  /data/web_static/releases/{archive_dir}/")

        # Uncompress the archive into the newly created directory
        run(f"tar -xzf /tmp/{archive_name}\
                -C /data/web_static/releases/{archive_dir}/")

        # Deletes the archive from the tmp directory
        run(f"rm /tmp/{archive_name}")

        # Move the content of the uncompressed archive
        # into its grand-parent directory
        run(f'rsync -aI /data/web_static/releases/{archive_dir}/{file_name}/*\
                /data/web_static/releases/{archive_dir}/')

        # Delete the empty archive directory
        run(f'rm -rf /data/web_static/releases/{archive_dir}/{file_name}')

        # Deletes the symbolic link /data/web_static/current
        # from the web server
        run(f"rm -rf /data/web_static/current")

        # Recreates a new the symbolic link
        run(f"ln -s /data/web_static/releases/{archive_dir}/\
                /data/web_static/current")

        # Reload the server
        run('sudo service nginx restart')

    except Exception as e:
        print(e)
        return False

    print('New version deployed!')
    return True
