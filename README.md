# ansible-elasticsearchCluster
For this use case, we will use Vagrant to build a Local or Development elasticsearch cluster and AWS to build a Production-like setup of an ElasticSearch cluster with 5 nodes for HA distributed across multiple regions.

The deployment will use Docker microservice infra to deploy elasticsearch and orchestration will be achieved using Kubernetes.

Kibana will be used for Visualization and Prometheus will be used for basic monitoring 


# Development (or Local) setup with Vagrant
Prerequisites:
- Docker
- VirtualBox or any other VM provider (https://www.virtualbox.org/wiki/Downloads)
- Vagrant (https://www.vagrantup.com/downloads.html)
- Ansible (https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
