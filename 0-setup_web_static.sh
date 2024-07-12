#!/usr/bin/env bash
# This script sets up web servers for deployment of static files

content="<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>                                                            </html>"

conf="server {                                                                     listen 80 default_server;                                            listen [::]:80 default_server;
	root /var/www/html;
	index index.html index.htm index.nginx-debian.html;

        server_name _;

        location / {
                try_files \$uri \$uri/ =404;
        }
        location /hbnb_static/ {
                alias /data/web_static/current/;
                try_files \$uri \$uri/ =404;
        }
}"

sudo apt-get -y update

if ! command -v nginx > /dev/null; then
        sudo apt-get install -y nginx;
        sudo service nginx start;
else
        sudo service nginx restart;
fi

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
sudo echo "$content" | sudo tee /data/web_static/releases/test/index.html > /dev/null
ln -sf /data/web_static/releases/test/ /data/web_static/current/
sudo echo "$conf" | sudo tee /etc/nginx/sites-available/default > /dev/null
sudo chown -R ubuntu:ubuntu /data/
sudo service nginx restart
