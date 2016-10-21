#!/bin/bash

if [ $# -lt 1 ]; then
    # Ubuntu
    dir=/var/www/html
    user=www-data
    arg1=ubuntu
elif [ $1 == 'arch' ]; then
    # Arch Linux
    dir=/srv/http
    user=http
    arg1=arch
else
    # Ubuntu
    dir=/var/www/html
    user=www-data
    arg1=ubuntu
fi

if [ $(whoami) == "root"  ]; then
    sudo /srv/daemons/runfunclistener.py &
    sudo -u $user /srv/daemons/tests.py
else
    sudo $0 $arg1
fi
