#!/bin/bash

# Copy dokku-plugins folder to remote server
scp -P 3033 -r ../dokku-plugins/ root@192.168.100.63:~

ssh -p 3033 root@192.168.100.63 << EOF
  cd ~
  sudo dokku plugin:uninstall pr-db-mongo
  chmod +x ~/dokku-plugins/pr-db-mongo/dependencies
  mv ~/dokku-plugins/pr-db-mongo /var/lib/dokku/plugins/available
  dokku plugin:enable pr-db-mongo
  sudo dokku plugin:install-dependencies
  sudo dokku plugin:install
EOF

