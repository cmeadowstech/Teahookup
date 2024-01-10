#!/bin/bash
set -e

# https://www.joseferben.com/posts/django-on-flyio/

# Set up swapping
fallocate -l 512M /swapfile
chmod 0600 /swapfile
mkswap /swapfile
echo 10 > /proc/sys/vm/swappiness
swapon /swapfile

gunicorn config.wsgi:application -b 0.0.0.0:8000 --workers=2 --capture-output --enable-stdio-inheritance