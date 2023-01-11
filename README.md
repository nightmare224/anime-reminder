The automated-deploy-tool contain `vagrant` and `ansible` parts.

`vagrant` would create a cluster which contains two VMs (one master node and one worker node) on VMWare.

`ansible` would deploy the Kubenetes on the cluster, and then deploy `infra-service` and `app-service`.

The `infra-service` is the service that require for almost every kind of application including `calico`, `metallb`, `ingress-nginx`, `longhorn`, etc.

The `app-service` is the application itself.