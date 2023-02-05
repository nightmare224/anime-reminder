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

### Usage

After all the services is running, access https://sc23.group40.io to see your Anime Reminder.

**Note**: Remember to add the mapping of **sc23.group40.io** to **LB_EXTERNEL_IP**  in `/etc/hosts` before access the web application.



## Features

### Architecture

The components in the Kubernetes cluster that would be deployed by Ansible are briefly shown as below:

<img src="https://github.com/nightmare224/anime-reminder/blob/master/docs/images/architecture.png" alt="architecture"/>

In this repository, you can find there are four directories: [**app-service**](https://github.com/nightmare224/anime-reminder/tree/master/app-service), [**infra-service**](https://github.com/nightmare224/anime-reminder/tree/master/infra-service), [**monitor-service**](https://github.com/nightmare224/anime-reminder/tree/master/monitor-service), and [**automated-deploy-tool**](https://github.com/nightmare224/anime-reminder/tree/master/automated-deploy-tool) which are corresponding to the picture.

***

### app-service

The Anime Reminder application is composed of four components which is **Keycloak**, **PostgreSQL**, **UI**, and **API.** 

#### Manually Install

The helm chart of our application which contains these 4 components can be found [here](https://github.com/nightmare224/anime-reminder/tree/master/app-service/anime-reminder/helm). To deploy this anime-reminder helm chart manually not by Ansible, you can execute below command in k8s master node:

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

If you would like to visit the Keycloak, access https://sc23.group40.io/auth. The default keycloak admin username/password is **admin**/**admin**.

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

There are two monitor tools would be installed in the cluster which is **K9s** and **Kubernetes Dashboard**

#### Manually Install

To deploy those services manually not by Ansible, run the `deploy.sh` in the directory of the service that you want to install in k8s master node:

```bash
bash anime-reminder/monitor-service/<SERVICE NAME>/deploy.sh
```

#### K9s

For convenience, we have already compiled the source code to the executable file in [here](https://github.com/nightmare224/anime-reminder/tree/master/monitor-service/k9s/files/k9s).

#### Kubernetes Dashboard

The helm chart of Kubernetes Dashboard is from [here](https://artifacthub.io/packages/helm/k8s-dashboard/kubernetes-dashboard).

If you would like to visit the Kubernetes Dashboard, access https://sc23.group40-monitor.io.

There are two service account for Kuberenets Dashboard, which is **app-developer** and **infra-developer**. The app-developer can only access the **anime-reminder namespace**. The infra-developer can access **all namespaces**.

To get the token of these service accounts, run the below command in master node:

```bash
kubectl -n kubernetes-dashboard create token <SERVICE ACCOUNT>
```



***

### automated-deploy-tool

There are two parts in these folder: Vagrant and Ansible.

#### Vagrant

This [Vagrantfile](https://github.com/nightmare224/anime-reminder/blob/master/automated-deploy-tool/vagrant.nosync/Vagrantfile) would create three virtual machines on VMWare. Each of them would have 2 CPU cores and 4 Gi Memory. Those machine would get the IP Address by DHCP, so you would have to go check the IP Address by yourself after the VM created.

#### Ansible

As we introduce in [Install](https://github.com/nightmare224/anime-reminder#install) section, executing `bash anime-reminder/automated-deploy-tool/ansible/run.sh` would trigger the Ansible playbook to setup Kubernetes cluster on target machines and deploy [**app-service**](https://github.com/nightmare224/anime-reminder/tree/master/app-service), [**infra-service**](https://github.com/nightmare224/anime-reminder/tree/master/infra-service), and [**monitor-service**](https://github.com/nightmare224/anime-reminder/tree/master/monitor-service).

If you don't want the Ansible deploy everything, you can only tick the box you want to deploy in [**anime-reminder/automated-deploy-tool/ansible/taglist**](https://github.com/nightmare224/anime-reminder/blob/master/automated-deploy-tool/ansible/taglist).

For example, this would deploy all the components.

```
[v] k8s
[v] monitor-service
[v] infra-service
[v] app-service
```

and this would only deploy **monitor-service**.

```
[x] k8s
[v] monitor-service
[x] infra-service
[x] app-service
```

>k8s: Install and setup Kubernetes cluster on target machines
>
>monitor-service: K9s and Kubernetes Dashboard
>
>infra-service: Calico, Cert Manager, Ingress Nginx, Longhorn, and MetalLB
>
>app-service: Anime Reminder application including PostgreSQL, Keycloak, UI, and API.



## Test

Here we provide some scenario and command to test the ability of our application and its underly infrastruture.

### Update application after source code change

When we modify the source code in UI or API, we will have to **rebuild the docker image** and do **helm upgrade**.

After modified the code, follow below steps to rebuild and update.

1. Configure Docker username, password, image name, and image tag in [anime-reminder/app-service/anime-reminder/app/ui/config.ini](https://github.com/nightmare224/anime-reminder/blob/master/app-service/anime-reminder/app/ui/config.ini) or [anime-reminder/app-service/anime-reminder/app/api/config.ini](https://github.com/nightmare224/anime-reminder/blob/master/app-service/anime-reminder/app/api/config.ini)

   ```ini
   [BUILD-IMAGE-CONFIG]
     BUILD_IMAGE_NAME="nightmare224/anime-reminder-ui"
     BUILD_IMAGE_TAG="1.0.1"
     BUILD_NO_CACHE=false
     SRCCODE_PATH="src"
     WORKDIR_PATH="/opt"
     SERVICE_PORT=80
   
   [PUSH-IMAGE-CONFIG]
     DOCKER_USERNAME="nightmare224"
     DOCKER_PASSWORD="efreet224"
   ```

   ```ini
   [BUILD-IMAGE-CONFIG]
     BUILD_IMAGE_NAME="nightmare224/anime-reminder-api"
     BUILD_IMAGE_TAG="1.0.0"
     BUILD_NO_CACHE=false
     SRCCODE_PATH="src"
     WORKDIR_PATH="/opt"
     SERVICE_PORT=80
   
   [PUSH-IMAGE-CONFIG]
     DOCKER_USERNAME="nightmare224"
     DOCKER_PASSWORD="********"
   ```

2. Configure the image name and image tag in [anime-reminder/app-service/anime-reminder/helm/anime-reminder/values.yaml](https://github.com/nightmare224/anime-reminder/blob/master/app-service/anime-reminder/helm/anime-reminder/values.yaml)

   ```yaml
   ui:
     replicaCount: 2
     image:
       repository: nightmare224/anime-reminder-ui
       pullPolicy: Always
       tag: "1.0.1"
   ...
   
   api:
     replicaCount: 2
     image:
       repository: nightmare224/anime-reminder-api
       pullPolicy: Always
       tag: "1.0.0"
   
   ...
   ```

3. Build and update the application

   Through Ansilbe:

   ```bash
   bash anime-reminder/automated-deploy-tool/ansible/run.sh
   ```

   Manually in k8s master node:

   ```bash
   bash anime-reminder/app-service/anime-reminder/deploy.sh
   ```



### Network Policy Verify

We only allow Keycloak and API connection to PostgreSQL. We can verify this network policy by connecting to PostgreSQL through psql command in Keycloak, API, and UI pods.

After getting into a shell of a container, execute below command:

```bash
apt-get install postgresql-client -y
psql postgres://<PG USERNAME>:<PG PASSWORD>@ar-postgresql.anime-reminder.svc.cluster.local/animereminder
```

>If you didn't configure the username and password of PostgreSQL, the default username is **postgres** and the password is **pganimereminder**

In the pod of Keycloak and API, the connection with database would succeed. But in the pod of UI, it would timeout and failed.



### RBAC Verify

Visit Kuberenetes Dashboard at https://sc23.group40-monitor.io

First login as **app-developer**, the token can be generate by running below command in master node:

```bash
kubectl -n kubernetes-dashboard create token app-developer
```

The app-developer can only access anime-reminder namesapce.

And then login as infra-developer, the token can be generate by running below command in master node:

```bash
kubectl -n kubernetes-dashboard create token infra-developer
```

The infra-developer can only access all namesapces.
