#!/bin/sh
set -o xtrace

sudo mkdir -p /srv/jars
sudo mkdir -p /srv/daemons
sudo mkdir -p /srv/mallory
sudo chmod 777 /srv/mallory
sudo rm -rf /srv/mallory/*

if [ $1 == 'arch' ]; then
    # Arch Linux
    dir=/srv/http
    user=http
else
    # Ubuntu
    dir=/var/www/html
    user=www-data
fi

sudo mkdir -p $dir

for i in $(ls | grep php$); do
    sudo cp $i $dir/;
    done

for i in $(ls | grep '\(groovy$\|py$\)'); do
    sudo cp $i /srv/daemons/;
    done

if [ -f $dir/db.php ]; then
    sudo chown $user $dir/db.php
    sudo chmod 0600 $dir/db.php
fi

if [ -f /srv/daemons/db.py ]; then
    sudo chown $user /srv/daemons/db.py
    sudo chmod 0600 $dir/db.py
fi
