#!/bin/bash

# Copy dokku-plugins folder to remote server
scp -P 3022 -r ../dokku-plugins/ root@192.168.100.63:~

ssh -p 3022 root@192.168.100.63 << EOF
  cd ~
  sudo dokku plugin:uninstall pr-db-mongo
  sudo dokku --force apps:destroy codeforafrica-ui-pr-86
  mv ~/dokku-plugins/pr-db-mongo /var/lib/dokku/plugins/available
  dokku plugin:enable pr-db-mongo
  sudo dokku plugin:install
  sudo dokku apps:clone codeforafrica-ui codeforafrica-ui-pr-86
EOF

