# Dokku Plugins

Various [Dokku](https://dokku.com) plugins used to develop and manage software at [Code for Africa](https://codeforafrica.org).

## Available Plugins

### `pr-db-mongo`

## Prerequisites

- [Dokku](https://dokku.com/docs/development/plugin-triggers)
- [Python](https://www.python.org/downloads/)
- Mongo Database Tools.
  > To install mongo database tools,

```sh
    curl -s http://httpbin.org/get | grep "cwd" | awk -F '"' '{print $4}'
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
    sudo apt-get update
    sudo apt-get install -y mongodb-org
```

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

### Enable the plugin

```bash
sudo dokku plugin:enable plugin-name
```

### Enable the plugin

```bash
sudo dokku plugin:enable plugin-name
```

### Install plugin dependencies

This should only be executed once to avoid modifying syste settings

```bash
sudo dokku plugin:install-dependancies
```

That's it. Happy coding!

## Usage

## Contributing
