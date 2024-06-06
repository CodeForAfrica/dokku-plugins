import subprocess
import sys
from urllib.parse import quote_plus, urlsplit

PLUGIN_NAME = "pr-db-mongo"


def execute_bash(command, **kwargs):
    return subprocess.run(command, check=True, capture_output=True, text=True, *kwargs)


def get_uri(db_url, db_name=""):
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


def configure_pr_app(original_mongodb_url, app_name):
    mongodb_url = get_uri(original_mongodb_url, app_name)
    app_url = f"PAYLOAD_PUBLIC_APP_URL=https://{app_name}.dev.codeforafrica.org"
    commands = [
        ["dokku", "config:set", "--no-restart", app_name, app_url],
        ["dokku", "config:set", "--no-restart",
            app_name, f"MONGODB_URL={mongodb_url}"],
        # TODO: get main domain from original app and modify it
        ["dokku", "domains:add", app_name,
            f"{app_name}.dev.codeforafrica.org"],
        ["dokku", "letsencrypt:enable", app_name],
    ]
    for command in commands:
        execute_bash(command)


def clone_pr_database(original_mongodb_url, app_name):
    split_url = urlsplit(original_mongodb_url)
    source = split_url.path.lstrip("/")
    uri = get_uri(original_mongodb_url)
    command1 = [f"mongodump", "-vvvvv", "--archive",
                f"--uri={uri}", f"--db={source}",]
    command2 = [f"mongorestore", "-vvvvv", f"--uri={uri}", "--archive",
                f"--nsFrom={source}.*", f"--nsTo={app_name}.*", f"--nsInclude={source}.*"]
    proc1 = subprocess.Popen(command1, stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(command2, stdin=proc1.stdout)

    proc1.stdout.close()
    proc2.communicate()


def setup_pr_app(original_mongodb_url, app_name):
    print(f"{PLUGIN_NAME}: setting up '{app_name}' ... ", end="")
    try:
        clone_pr_database(original_mongodb_url, app_name)
        configure_pr_app(original_mongodb_url, app_name)

        print("done")
    except Exception as e:
        print("failed")
        print(f"{PLUGIN_NAME}:", e)
        sys.exit(1)


def delete_pr_database(original_mongodb_url, db_name):
    print(f"{PLUGIN_NAME}: deleting database '{db_name}' ... ", end="")
    try:
        uri = get_uri(original_mongodb_url, db_name)
        command = ["mongosh", uri, "--eval", "db.dropDatabase()"]
        execute_bash(command)

        print("done")
    except Exception as e:
        print("failed")
        print(f"{PLUGIN_NAME}:", e)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(f"{PLUGIN_NAME} <dokku app name> <setup|delete> ({sys.argv})")
    action = sys.argv[2].lower()
    if action not in ["setup", "delete"]:
        sys.exit(f"{PLUGIN_NAME} <dokku app name> <setup|delete>")
    app_name = sys.argv[1]
    app_name_pr_number = app_name.split("-pr-")
    if len(app_name_pr_number) == 2:
        original_app_name = app_name_pr_number[0].strip()
        command = ["dokku", "config:get", original_app_name, "MONGODB_URL"]
        original_mongodb_url = execute_bash(command).stdout.strip()
        if original_mongodb_url:
            if action == "setup":
                setup_pr_app(original_mongodb_url, app_name)
            else:  # action == "delete":
                delete_pr_database(original_mongodb_url, app_name)
        # else: no MONGODB_URL found, silently skip
    # else: app doesn't follow naming convention, silently skip
