#!/usr/bin/python3
"""AirBnB application Fabfile

This is meant for AirBnB application deployment
and mainteneance

Notes:
    * This is for application deployment
    * Also, for application mainteneance
    * MUST not be used for server-state management
"""

from dataclasses import dataclass
from fabric.api import get, hide, local, parallel, put, run, settings, sudo, task, env
from fabric.decorators import hosts, roles
from paramiko import hostkeys


@dataclass(frozen=True)
class SERVER:
    MAIN = 'alexa.server'
    SECONDARY = 'alexa.sec.server'
    LOAD_BALANCER = 'alexa.lb.server'
    DB = 'alexa.server'


env.hosts = [
    SERVER.MAIN,
    SERVER.SECONDARY,
    SERVER.DB,
    SERVER.LOAD_BALANCER
]

env.roledefs = {
    'db': [SERVER.MAIN],
    'web': [SERVER.MAIN, SERVER.SECONDARY],
    'lb': [SERVER.LOAD_BALANCER]
}

env.use_ssh_config = True

@task
def status():
    commands = {
        "Disk Usage": "df -h",
        "Memory Usage": "free -h",
        "CPU Usage": "top -bn1 | grep 'Cpu(s)'",
        "Users Connected": "w",
        "Uptime": "uptime"
    }

    for title, command in commands.items():
        try:
            result = run(command, quiet=True)
            print(f"\n{title}:")
            print(format_std_result(result))
        except Exception as e:
            print(f"Failed to execute {title}: {e}")
    print("")

@task(name='lb-status')
@roles('lb')
def load_balancer_state(all: bool = False):
    """Get load balancer state: all<bool>

    Args:
        all: For full state

    Ugsage: fab load_balancer_state
            fab load_balancer_state:all=True for full state
    """
    if all:
        status()
    with hide('running', 'warnings'):
        print("Checking HAProxy status...")
        result = run('systemctl is-active haproxy', quiet=True)
        print(format_std_result(result))

@task
@hosts([SERVER.MAIN])
def test_file():
    result = put('README.md', '/README.md', use_sudo=True)
    if result.failed:
        return
    sudo(f'tar -czvf {"README"}.tar.gz {"~/README.md"}')


def format_std_result(output):
    return output.stdout.strip()
