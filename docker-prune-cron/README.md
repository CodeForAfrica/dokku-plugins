# Docker Image Pruning Cron Job for Dev server

This README provides instructions for setting up a cron job to regularly prune old Docker images on a Dev server. Pruning Docker images helps to manage disk space effectively by removing unused images.

## Prerequisites

- SSH access to the Dev server.

## Steps to Set Up the Cron Job

### 1. Access the Dev Server

SSH into your Dev server:

```sh
ssh azureuser@ui-1.dev.codeforafrica.org
```


### 2. Set Up the Cron Job

Edit the cron table to schedule the pruning job every 4 hours.

Open the crontab for editing:

```sh
crontab -e
```

Add the following line to schedule the job:

```
0 */4 * * * /home/azureuser/prune_docker_images.sh
```

### 3. Verify the Cron Job

List the current cron jobs to ensure your job is added:

```sh
crontab -l
```
You can also check the logged output:

```sh

cat docker_prune_cron.log
```

## Troubleshooting

Check cron service status to ensure the cron service is running:

```sh
systemctl status cron
```

#### Check Syslog for Errors

If the cron job doesn’t seem to run, check the syslog for cron errors:

```sh
grep CRON /var/log/syslog
```
