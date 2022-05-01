# scripts

USAGE:
_kill_processes tool_name

_find_args toole_name arg 
example 1: _find_args grep l
example2 : _find_args "docker run" -a

_docker_killer n
# this script remove last n containers and images, from which these containers were created
example 1: _docker_killer 5 # kill last 5 containers and images, from which these containers were created
