#!/bin/sh
set -o xtrace

sudo mkdir -p /srv/jars
sudo chown root /srv/jars
sudo chgrp root /srv/jars
sudo mkdir -p /srv/daemons
sudo chown root /srv/daemons
sudo chgrp root /srv/daemons

if [ $# -lt 1 ]; then
    # Ubuntu
    dir=/var/www/html
    user=www-data
    os=ubuntu
elif [ $1 == 'arch' ]; then
    # Arch Linux
    dir=/srv/http
    user=http
    os=arch
else
    # Ubuntu
    dir=/var/www/html
    user=www-data
    os=ubuntu
fi

sudo mkdir -p $dir
sudo touch /srv/res
sudo chown $user /srv/res
sudo chmod 0600 /srv/res

sudo mkdir -p /srv/mallory
sudo chown $user /srv/mallory
# The sticky bit will prevent this folder from getting deleted by mallory
sudo chmod 1777 /srv/mallory

for i in $(ls | grep php$); do
    sudo cp $i $dir/;
    done

sudo cp -r api $dir/

for i in $(ls | grep '\(groovy$\|py$\)'); do
    sudo cp $i /srv/daemons/;
    done

if [ -f $dir/db.php ]; then
    sudo chown $user $dir/db.php
    sudo chmod 0600 $dir/db.php
fi

if [ -f /srv/daemons/db.py ]; then
    sudo chown $user /srv/daemons/db.py
    sudo chmod 0600 /srv/daemons/db.py
fi

if [ $os == "arch" ]; then
    sudo systemctl restart httpd
else
    # One of them should work...
    sudo systemctl restart apache2
    sudo service apache2 restart
fi
