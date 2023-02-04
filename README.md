# Anime Reminder

## Introduction
Anime Reminder is a web application for recording the season and episode of anime you had watched. 
Register your own account and create your own anime list and keep track of your progress.

Besides the web application itself, Anime Reminder provide the [Ansible](https://github.com/ansible/ansible) playbook to build the Kubernetes cluster and deploy the required infrastrature on it.

## Quick Started
### Prerequisite

1. Prepare at least two target machines with **Ubuntu 20.04** operating system under **ARM64** architecture

   > We also provide the [Vagrantfile](https://github.com/nightmare224/anime-reminder/blob/master/automated-deploy-tool/vagrant.nosync/Vagrantfile) to install 3 virtual machine in VMWare on M1 MacOS.

2. The target machines need to enable SSH connection.

3. The target machines need to have 2 CPU cores and 4 Gi memory.

### Install

To install Anime Reminder, follow the below steps:

1. **Clone the Anime Reminder repository**

   ```bash
   git clone https://github.com/nightmare224/anime-reminder.git

2. **Install Ansible**

   Please follow the step in [Ansible documentation](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) to install Ansible on the node that is able to connect with target machines.

3. **Configure the [anime-reminder/automated-deploy-tool/anisble/inventory](https://github.com/nightmare224/anime-reminder/blob/master/automated-deploy-tool/ansible/inventory) file**

   Setup the IP address and username and password of the target machines.

   **IMPORTANT**: Only modify the **ansible_host**, **ansible_user**, and **ansible_password** these three field. Do not change other parts.

   ```ini
   [master]
   k8s-master ansible_host=192.168.2.185 ansible_user=vagrant ansible_password=vagrant
   
   [worker]
   k8s-worker1 ansible_host=192.168.2.186 ansible_user=vagrant ansible_password=vagrant
   k8s-worker2 ansible_host=192.168.2.187 ansible_user=vagrant ansible_password=vagrant
   ```

4. **Configure load balancer IP Address for MetalLB in [anime-reminder/infra-service/metallb/config.ini](https://github.com/nightmare224/anime-reminder/blob/master/infra-service/metallb/config.ini)**

   As we are bare metal cluster, we have to setup the load balancer by ourselves. Set **LB_EXTERNEL_IP** to the IP Address that you want to used it as external IP.

   ```ini
   [SERVICE-CONFIG]
     HELM_TEMPLATE_PATH="helm/metallb/"
     SERVICE_NAME="metallb"
     SERVICE_NAMESPACE="metallb-system"
     LB_EXTERNEL_IP="192.168.0.112"
   ```

5. **Deploy Anime Reminder**

   Run the `run.sh` in Anime Reminder repository. This would create Kubernetes cluster on target machines, deploy required infrastatrue services for example `MetalLB`, `ingress controller`, `longhorn`, etc., and deploy Anime Reminder application.

   ```bash
   bash anime-reminder/automated-deploy-tool/ansible/run.sh
   ```



## Features

### Architecture
![architecture](https://github.com/nightmare224/anime-reminder/tree/master/docs/images/architecture.png)


In this repository, you can see four directories which is [**app-service**](https://github.com/nightmare224/anime-reminder/tree/master/app-service), [**automated-deploy-tool**](https://github.com/nightmare224/anime-reminder/tree/master/automated-deploy-tool), [**infra-service**](https://github.com/nightmare224/anime-reminder/tree/master/infra-service), and [**monitor-service**](https://github.com/nightmare224/anime-reminder/tree/master/monitor-service).

### App-service
The Anime Reminder application is composed of four components which is **Keycloak**, **PostgreSQL**, UI frontend, and API backend.




