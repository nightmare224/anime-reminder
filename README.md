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

The components in the Kubernetes cluster that would be deployed by Ansible are briefly shown as below:

<img src="https://github.com/nightmare224/anime-reminder/blob/master/docs/images/architecture.png" alt="architecture"/>

In this repository, you can find there are four directories: [**app-service**](https://github.com/nightmare224/anime-reminder/tree/master/app-service), [**infra-service**](https://github.com/nightmare224/anime-reminder/tree/master/infra-service), [**monitor-service**](https://github.com/nightmare224/anime-reminder/tree/master/monitor-service), and [**automated-deploy-tool**](https://github.com/nightmare224/anime-reminder/tree/master/automated-deploy-tool) which are corresponding to the picture.

***

### app-service

The Anime Reminder application is composed of four components which is **Keycloak**, **PostgreSQL**, **UI**, and **API.** 

#### Manually Install

The helm chart of our application which contains these 4 components can be found [here](https://github.com/nightmare224/anime-reminder/tree/master/app-service/anime-reminder/helm). To deploy this anime-reminder helm chart manually not by Ansible, you can execute:

```bash
bash anime-reminder/app-service/anime-reminder/deploy.sh
```

If you would like to change the username and password of PostgreSQL and Keycloak, change the value of **[POSTGRESQL-CONFIG]** and **[KEYCLOAK-CONFIG]** section in [anime-reminder/app-service/anime-reminder/config.ini](https://github.com/nightmare224/anime-reminder/blob/master/app-service/anime-reminder/config.ini) before you run `deploy.sh`.

```ini
[SERVICE-CONFIG]
  HELM_TEMPLATE_PATH="helm/anime-reminder/"
  SERVICE_NAME="anime-reminder"
  SERVICE_NAMESPACE="anime-reminder"
  DOMAIN_NAME="sc23.group40.io"

[POSTGRESQL-CONFIG]
  POSTGRESQL_USER="postgres"
  POSTGRESQL_PASSWORD="pganimereminder"

[KEYCLOAK-CONFIG]
  KEYCLOAK_USER="admin"
  KEYCLOAK_PASSWORD="admin"
```

#### Keycloak

The helm chart of Keycloak is based on [codecentric/keycloak](https://artifacthub.io/packages/helm/codecentric/keycloak). We add some our own configuration and then merge it in to our anime-reminder helm chart.

#### PostgreSQL

The helm chart of PostgreSQL is based on [cetic/postgresql](https://artifacthub.io/packages/helm/cetic/postgresql). We add some our own configuration and then merge it in to our anime-reminder helm chart.

#### UI

The UI of anime-reminder is developed in Python Flask framework. The source code can be found in [**anime-reminder/app-service/anime-reminder/app/ui**]( https://github.com/nightmare224/anime-reminder/tree/master/app-service/anime-reminder/app/ui).

#### API

The API of anime-reminder is developed in Python Flask framework. The source code can be found in [**anime-reminder/app-service/anime-reminder/app/api**]( https://github.com/nightmare224/anime-reminder/tree/master/app-service/anime-reminder/app/api).

***

### infra-service

There are several infrastature services underlay Anime Reminder application which is **Calico**, **MetalLB**, **Ingress Nginx**, **Longhorn**, and **Cert Manager**.

#### Manually Install

To deploy those services manually not by Ansible, run the `deploy.sh` in the directory of the service that you want to install:

```bash
bash anime-reminder/infra-service/<SERVICE NAME>/deploy.sh
```

#### Calico

The helm chart of Calico is from [here](https://artifacthub.io/packages/helm/projectcalico/tigera-operator).

#### MetalLB

The helm chart of MetalLB is from [here](https://artifacthub.io/packages/helm/metallb/metallb).

#### Ingress Nginx

The yaml file of Ingress Nginx is from [here](https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.5.1/deploy/static/provider/aws/deploy.yaml).

#### Longhorn

The helm chart of Longhorn is from [here](https://artifacthub.io/packages/helm/longhorn/longhorn).

#### Cert Manager

The helm chart of Cert Manager is from [here](https://artifacthub.io/packages/helm/cert-manager/cert-manager).

***

### monitor-service

There are two monitor tool would be installed in the cluster which is **K9s** and **Kubernetes Dashboard**

#### Manually Install

To deploy those services manually not by Ansible, run the `deploy.sh` in the directory of the service that you want to install:

```bash
bash anime-reminder/monitor-service/<SERVICE NAME>/deploy.sh
```

#### K9s

For convenience, we have already compiled the source code to the executable file in [here]().

#### Kubernetes Dashboard

The helm chart of Kubernetes Dashboard is from [here](https://artifacthub.io/packages/helm/k8s-dashboard/kubernetes-dashboard).

There are two service account for Kuberenets Dashboard, which is **app-developer** and **infra-developer**. The app-developer can only access the **anime-reminder namespace**. The infra-developer can access **all namespaces**.

To get the token of these service accounts, run the below command in master node:

```bash
kubectl -n kubernetes-dashboard create token <SVCACCT>
```

