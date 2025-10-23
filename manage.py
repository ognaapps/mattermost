#!/usr/bin/env python3
import subprocess
import sys
import secrets
import string

PROJECT_NAME = "mattermost"


def generate_clear_password(length=100):
    ambiguous = {'O', '0', 'I', 'l', '1'}
    alphabet = ''.join(c for c in (string.ascii_letters + string.digits) if c not in ambiguous)
    return ''.join(secrets.choice(alphabet) for _ in range(length))


env_variables = {
    'POSTGRES_USER': lambda x: f"{x}=matter_postgres_users",
    'POSTGRES_PASSWORD': lambda x: f"{x}={generate_clear_password()}",
    'POSTGRES_DB': lambda x: f"{x}=postgres",
    'MM_SERVICESETTINGS_SITEURL': f"https://{PROJECT_NAME}.user.ognastack.com"
}


def configure():
    with open('.env', 'w+') as env_file:
        for key, value in env_variables.items():
            if callable(value):  # check if it's a function/lambda
                result = value(key)
            else:
                result = f"{key}={value}"

            env_file.write(result)
            env_file.write("\n")


def up():
    """Start docker compose services"""
    configure()
    subprocess.run(["docker", "compose", "-p", PROJECT_NAME, "up", "-d"])


def down():
    """Stop docker compose services and remove volumes"""
    subprocess.run(["docker", "compose", "-p", PROJECT_NAME, "down", "-v"])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py [up|down]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "up":
        up()
    elif command == "down":
        down()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: up, down")
        sys.exit(1)
