import subprocess


def pip_install(dependancy):
    try:
        subprocess.check_call(["pip", "install", dependancy])
    except subprocess.CalledProcessError:
        print("Failed to install '{dependancy}'")


def execute_bash(command):
    try:
        return subprocess.run(
            command, check=True, stdout=subprocess.PIPE, text=True
        ).stdout.replace("\n", "")
    except Exception as e:
        print("Failed to execute '{command}'", e)
        return None
