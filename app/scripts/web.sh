#!/bin/bash
set -e

# Set up swapping
fallocate -l 512M /swapfile
chmod 0600 /swapfile
mkswap /swapfile
echo 10 > /proc/sys/vm/swappiness
swapon /swapfile

gunicorn config.wsgi:application -b 0.0.0.0:8080 --workers=2 --capture-output --enable-stdio-inheritance