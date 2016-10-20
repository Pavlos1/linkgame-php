#!/bin/sh
set -o xtrace

sudo mkdir -p /srv/jars
sudo mkdir -p /srv/daemons

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
