#!/bin/sh
set -o xtrace

./killdaemons.sh

if [ -f db.py ]; then
    chmod 0600 db.py
fi

if [ -f db.php ]; then
    chmod 0600 db.php
fi

if [ -f sol.txt ]; then
    chmod 0600 sol.txt
fi

sudo mkdir -p /srv/jars
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

sudo chown $user /srv/jars
sudo chgrp $user /srv/jars
sudo chmod 0700 /srv/jars

sudo touch /srv/whoami
sudo chown $user /srv/whoami
sudo chmod 0600 /srv/whoami
echo $user | sudo tee /srv/whoami > /dev/null

sudo mkdir -p $dir
sudo rm -f /srv/res
sudo rm -f /srv/rest
sudo touch /srv/res
sudo touch /srv/rest
sudo chown $user /srv/res
sudo chmod 0600 /srv/res
sudo chown $user /srv/rest
sudo chmod 0600 /srv/rest

sudo mkdir -p /srv/mallory
sudo chown $user -R /srv/mallory
sudo mkdir -p /srv/malloryt
sudo chown $user -R /srv/malloryt
# The sticky bit will prevent this folder from getting deleted by mallory
sudo chmod 1777 /srv/mallory
sudo chmod 1777 /srv/malloryt

for i in $(ls | grep php$); do
    sudo cp $i $dir/;
    done

sudo cp -r api $dir/
sudo cp sol.txt /srv/
sudo chown $user /srv/sol.txt
sudo chmod 0600 /srv/sol.txt

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

sudo iptables -A OUTPUT -p all -m owner --uid-owner mallory -j DROP
sudo iptables -A OUTPUT -p all -m owner --uid-owner malloryt -j DROP

if [ $os == "arch" ]; then
    sudo systemctl restart httpd
else
    # One of them should work...
    sudo systemctl restart apache2
    sudo service apache2 restart
fi
