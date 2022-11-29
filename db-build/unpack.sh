#!/usr/bin/bash

# Script to unpack and restore mariadb backups
# This should be placed in the /docker-entrypoint-initdb.d
# with a related mariadb backup

cd /tmp
rm -rf /var/lib/mysql
zstd -d -c music.zst | mbstream -x
mariabackup --prepare --target-dir=/tmp
mariabackup --move-back --target-dir=/tmp
