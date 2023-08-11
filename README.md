# dokku-pr-delete-db-mongo Dokku Plugin

This repository contains a script designed to efficiently manage the deletion of preview applications. These applications follow a defined naming convention. As part of the deletion process, the script ensures that the corresponding database, which is named identically to the app, is properly handled. The database, typically powered by MongoDB, is required for the app's functionality. The script verifies that the database is running on a specific server, which is identified by a URL sourced from a predefined configuration. This streamlined process ensures that both the preview app and its associated database are effectively and consistently managed, facilitating the organization's development workflows.

## Prerequisites

- [Dokku](https://dokku.com/docs/development/plugin-triggers)
- [Python](https://www.python.org/downloads/)

## Installation

```bash
dokku plugin:install https://github.com/CodeForAfrica/dokku-pr-delete-db-mongo
```

## Usage

### Environment Variables

## Contributing

To contribute, clone the repository and add your scripts
