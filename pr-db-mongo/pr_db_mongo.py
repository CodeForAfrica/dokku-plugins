import subprocess
import sys
from urllib.parse import urlsplit

import pymongo

PLUGIN_NAME = "pr-db-mongo"

def execute_bash(command):
    return subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True
    )

def configure_pr_app(app_name, db_url):
    print(f"{PLUGIN_NAME}: configuring '{app_name}' ... ", end="")

    try:
        commands = [
            ["dokku", "config:set", "--no-restart", app_name, f"MONGODB_URL={db_url}"],
            # TODO: get main domain from original app and modify it
            ["dokku", "domains:add", app_name, f"{app_name}.dev.codeforafrica.org"],
            ["dokku", "letsencrypt:enable", app_name],
        ]
        for command in commands:
            execute_bash(command)

        print("done")
    except Exception as e:
        print("failed")
        print(f"{PLUGIN_NAME}:", e)
        sys.exit(1)


def delete_pr_database(db_name, db_url):
    print(f"{PLUGIN_NAME}: deleting database '{db_name}' ... ", end="")

    try:
        parsed_url = urlsplit(db_url)
        username = parsed_url.username
        password = parsed_url.password
        host = parsed_url.hostname
        port = parsed_url.port
        client = pymongo.MongoClient(
            host=host, port=port, username=username, password=password
        )
        client.drop_database(db_name)

        print("done")
    except Exception as e:
        print("failed")
        print(f"{PLUGIN_NAME}:", e)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(f"{PLUGIN_NAME} <dokku app name> <create|delete> ({sys.argv})")
    action = sys.argv[2].lower()
    if not action in ["create", "delete"]:
        sys.exit(f"{PLUGIN_NAME} <dokku app name> <create|delete>")
    app_name = sys.argv[1]
    app_name_pr_number = app_name.split("-pr-")
    if len(app_name_pr_number) == 2:
        original_app_name = app_name_pr_number[0].strip()
        command = ["dokku", "config:get", original_app_name, "MONGODB_URL"]
        mongodb_url = execute_bash(command)
        if mongodb_url:
            if action == "create":
                configure_pr_app(app_name, mongodb_url)
            else: # action == "delete":
                delete_pr_database(app_name, mongodb_url)
        # else: no MONGODB_URL found, silently skip
    # else: app doesn't follow naming convention, silently skip
