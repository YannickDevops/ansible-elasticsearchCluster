# ansible-ELK Cluster in Docker
For this use case, we will use Vagrant to build a Local or Development ELK cluster and AWS to build a Production-like setup  with 5 nodes for High Availability and Fault tolerance.

The deployment will use Docker infra to deploy the stack and orchestration will be achieved using Kubernetes.

Kibana will be used for Visualization and Prometheus will be used for basic monitoring 


# Development (or Local) setup with Vagrant
Prerequisites:
- VirtualBox (https://www.virtualbox.org/wiki/Downloads)
- Vagrant (https://www.vagrantup.com/downloads.html)
- Ansible (https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

In this configuration, we are deploying 6 Docker containers. Each container is enabled with Elasticsearch, Kibana and Logstash.
In order to scale the number of any component, toggle from 0 to 1 in `deploy.yml`. Example:
```
env:
          LOGSTASH_START: 0
          ELASTICSEARCH_START: 1
          KIBANA_START: 0
```

Here, we will have one Master node enabled with ElasticSearch and Kibana and all worker nodes only with Elasticsearch, so to form a Cluster.

1. Run ```vagrant init``` to generate a template Vagrantfile
2. Add the following lines in the Vagrantfile:
``` config.vm.box = "centos/7" 
  config.vm.provision "ansible" do |ansible|
      ansible.playbook = "site.yml"
      ansible.groups = {
      "vagrant" => ["127.0.0.1"]
```
3. Clone this repository and change the following variables in the deploy.yml:
```
hosts: all
number of nodes: <to whatever you want>

```
4. Change the cluster name in ES configuration in `files/elasticsearch.yml` to `cluster.name: logging`
5. In inventories/hosts, insert your own hostname or fqdn
6. Run: `ansible-playbook site.yml -u ec2-user`
7. This will build an ElasticSearch Cluster completely dockerized and a Kibana dashboard for Visualization.


# Testing my Stack using Python in Docker

The Python script is found in dir `python-docker-test`. 
The following command will execute these steps:
1. Copy all the configuration files (Dockerfile, scripts, etc...) to target host
2. Build the image with the version found in `vars: v1` in the `python-docker.yml` playbook
3. Deploy the container and keep indexing ES with data (Courtesy of https://swapi.co/api/people)

Run: `ansible-playbook python-docker-test/python-docker.yml  --private-key=test-key.pem -u ec2-user`

NB: The container will exit if ES is not running!!


# TLS Encryption for Kibana
In case we would like to use TLS in Kibana, 2 architectures seems viable to me: 
1. Using Nginx as a Loadbalancer and offloading SSL at Nginx
2. Configure Kibana.yml to only accept HTTPS requests. 

Clearly, the first option would be the best for this example, I will use the second option
Steps:
1. Generate certificates (as in dir kibana/certs)
2. Update kibana.yml:
```buildoutcfg
server.name: "my-kibana"
server.host: "kibana.local"
server.ssl.enabled: true
server.ssl.certificate: certs/kibana.crt
server.ssl.key: config/certs/new.cert.key
elasticsearch.url: "https://ec2-35-180-158-38.eu-west-3.compute.amazonaws.com:9200"
elasticsearch.username: "kibana"
elasticsearch.password: "kibana"
elasticsearch.ssl.certificateAuthorities: [ "certs/kibana.crt" ]
```
3. Mount the volume to Kibana docker and connect to kibana on https Port


### Adding Kubernetes to orchestrate all my containers
We will use Ansible to install Kubernetes and all its components (kubelet, kubectl, kubeadm and kubernetes-cni) 
- The role of the node will act as both the master node and the worker node 

Steps to install Kubernetes on Target hosts:
1. Install role on AnsibleController: `ansible-galaxy install grycap.kubernetes -p ../roles`
2. Run: `ansible-playbook install-k8s.yml --private-key=test-key.pem -u ec2-user`

Run Kubernetes deployment
1. Run: `ansible-playbook kubernetes.yml --private-key=test.pem -u ec2-user`


### Adding Prometheus for monitoring
1. Install Ansible role to deploy prometheus
Run: `ansible-galaxy install william-yeh.prometheus`
2. Install the Alertmanager for Prometheus
3. Configure scraping endpoints on port 9100 for node exporters

Metrics collected: CPU, Memory, Disk and Network information