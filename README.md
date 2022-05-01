# scripts

**USAGE:**

`_kill_processes tool_name`  

---

`_find_args tool_name arg`     
examples:  
`_find_args grep -l`  *#find in grep help message part with explanation -l arg*  
`_find_args "docker run" -a`  *#find in docker run help message part with explanation -l arg*  

---

`_docker_killer n`      
this script remove last n containers and images, from which these containers were created  
example:  
_docker_killer 5` *# kill last 5 containers and images, from which these containers were created*  

---
