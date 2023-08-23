import subprocess
import sys
from urllib.parse import quote_plus, urlsplit, urlunparse
import os

PLUGIN_NAME = "pr-db-mongo"


def execute_bash(command):
    return subprocess.run(command, check=True, capture_output=True, text=True)

def get_uri(db_url, db_name=''):
    split_url = urlsplit(db_url)
    username = split_url.username
    password = split_url.password
    scheme = split_url.scheme
    hostname = split_url.hostname
    port = split_url.port
    query = split_url.query
    credentials = ":".join([quote_plus(c) for c in (username, password)])
    host = f"{hostname}:{port}" if port else hostname
    options = f"/{db_name}?{query}" if query else ""
    return f"{scheme}://{credentials}@{host}{options}"

def configure_pr_app(uri, app_name):
    print(f"{PLUGIN_NAME}: configuring '{app_name}' ... ", end="")
    db_url = get_uri(uri, app_name)
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

def clone_pr_database(original_db_url, app_name):
    try:
        source = pymongo.uri_parser.parse_uri(original_db_url).get("database")
        uri = get_uri(original_db_url)
        command = ["mongodump", "-vvvvv", f"--archive", f"--uri={uri}", f"--db={source}", "|", "mongorestore", "-vvvvv", f"--uri={uri}", f"--archive", f"--nsFrom={source}.*", f"--nsTo={app_name}.*", f"--nsInclude={source}.*"]
        execute_bash(command)
    except Exception as e:
        print("failed to clone database")
        print(f"{PLUGIN_NAME}:", e)
        sys.exit(1)

def delete_pr_database(uri, db_name):
    print(f"{PLUGIN_NAME}: deleting database '{db_name}' ... ", end="")

    try:
        command=["mongosh", uri, "--eval", f"use {db_name}",  "--eval", "db.dropDatabase()"]
        execute_bash(command)

        print("done")
    except Exception as e:
        print("failed")
        print(f"{PLUGIN_NAME}:", e)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(f"{PLUGIN_NAME} <dokku app name> <create|delete> ({sys.argv})")
    action = sys.argv[2].lower()
    if action not in ["create", "delete"]:
        sys.exit(f"{PLUGIN_NAME} <dokku app name> <create|delete>")
    app_name = sys.argv[1]
    app_name_pr_number = app_name.split("-pr-")
    if len(app_name_pr_number) == 2:
        original_app_name = app_name_pr_number[0].strip()
        command = ["dokku", "config:get", original_app_name, "MONGODB_URL"]
        mongodb_url = execute_bash(command).stdout.strip()
        if mongodb_url:
            uri = get_uri(mongodb_url)
            if action == "create":
                clone_pr_database(mongodb_url, app_name)
                configure_pr_app(uri, app_name)
            else:  # action == "delete":
                delete_pr_database(uri=uri, db_name=app_name)
        # else: no MONGODB_URL found, silently skip
    # else: app doesn't follow naming convention, silently skip
