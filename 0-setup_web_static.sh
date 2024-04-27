#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static

sudo apt-get update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'
sudo mkdir -p /data
sudo mkdir -p /web_static
sudo mkidr -p /releases/test
sudo mkdir -p /data/web_static/shared
sudo mkdir -p /data/web_static/current

echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default

sudo service nginx restart

exit 0
