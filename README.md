# Dokku Plugins

Various [Dokku](https://dokku.com) plugins used to develop and manage software at [Code for Africa](https://codeforafrica.org).

## Available Plugins

### `pr-db-mongo`

## Prerequisites

- [Dokku](https://dokku.com/docs/development/plugin-triggers)
- [Python](https://www.python.org/downloads/)

## Installation

The .tgz installation via dokku plugin:install file://<path-to-tgz> or https://<path-to-tgz> seem to fail. We shall therefore use the manual installation until a fix is found.

### Copy the plugin(s) to dev
Copy the .tgz from the local/CI instance to the dev machine (running Dokku)
```bash
scp plugin.tgz user@remotehost:/path-to-copy-file
```
For example, if our plugin is called `pr-db-mongo`, then:
```bash
scp build/pr-db-mongo.tgz ubuntu@dev.codeforafrica.org:/~
```

### Make the plugin available to Dokku
ssh to the dev machine
```bash
ssh ubuntu@dev.codeforafrica.org:
```
Extract and copy plugin into `$PLUGIN_AVAILABLE_PATH`
```
tar -xf pr-db-mongo.tgz
chown dokku:dokku -R pr-db-mongo
mv pr-db-mongo /var/lib/dokku/plugins/available
```

### Install the plugin
```bash
sudo dokku plugin:enable pr-db-mongo
sudo dokku plugin:install
```

That's it. Happy coding!

## Usage

## Contributing
