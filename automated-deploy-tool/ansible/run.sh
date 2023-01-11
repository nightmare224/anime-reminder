#!/bin/bash
ansible-playbook playbook.yaml -i inventory -e 'ansible_python_interpreter=/usr/bin/python3'