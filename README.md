# RKE2 Ansible Role

[![Galaxy Quality](https://img.shields.io/ansible/quality/55229?style=flat&logo=ansible)](https://galaxy.ansible.com/lablabs/rke2)
[![Role version](https://img.shields.io/github/v/release/lablabs/ansible-role-rke2)](https://galaxy.ansible.com/lablabs/rke2)
[![Role downloads](https://img.shields.io/ansible/role/d/55229)](https://galaxy.ansible.com/lablabs/rke2)
[![GitHub Actions](https://github.com/lablabs/ansible-role-rke2/workflows/molecule%20test/badge.svg)](https://github.com/lablabs/ansible-role-rke2/actions)
[![License](https://img.shields.io/github/license/lablabs/ansible-role-rke2)](https://github.com/lablabs/ansible-role-rke2/blob/main/LICENSE)

[<img src="ll-logo.png">](https://lablabs.io/)

This Ansible role will deploy [RKE2](https://docs.rke2.io/) Kubernetes Cluster. RKE2 will be installed using the tarball method.  

The Role can install the RKE2 in 3 modes:

- RKE2 single node

- RKE2 Cluster with one Server(Master) node and one or more Agent(Worker) nodes

- RKE2 Cluster with Server(Master) in High Availability mode and zero or more Agent(Worker) nodes. In HA mode you should have an odd number (three recommended) of server(master) nodes that will run etcd, the Kubernetes API (Keepalived VIP address), and other control plane services.

## Requirements

* Ansible 2.10+

## Tested on

* CentOS 8
* Ubuntu 20.04 TLS

## Role Variables

This is a copy of `defaults/main.yml`

```yaml
# The node type - server or agent
rke2_type: server

# Deploy the cluster in HA mode
rke2_ha_mode: false

# Kubernetes API and RKE2 node registration IP address. The default Address is the IPv4 of the Server/Master node.
# In HA mode choose a static IP which will be set as VIP in keepalived.
rke2_api_ip: "{{ hostvars[groups.masters.0]['ansible_default_ipv4']['address'] }}"

# API Server destination port
rke2_apiserver_dest_port: 6443

# If false, server(master) node(s) will be schedulable and thus your workloads can get launched on them
rke2_server_taint: false

# Pre-shared secret token that other server or agent nodes will register with when connecting to the cluster
rke2_token: defaultSecret12345

# RKE2 version
rke2_version: v1.21.2+rke2r1

# URL to RKE2 repository
rke2_channel_url: https://update.rke2.io/v1-release/channels

# RKE2 channel
rke2_channel: stable

# Download Kubernetes config file to the Ansible controller 
rke2_download_kubeconf: false

# Do not deploy packaged components and delete any deployed components
# Valid items: rke2-canal, rke2-coredns, rke2-ingress-nginx, rke2-kube-proxy, rke2-metrics-server
rke2_disable:

# Path to custom manifests deployed during the RKE2 installation
rke2_custom_manifests:

# Deploy RKE2 and set the custom containerd images registries
rke2_custom_registry: false

# (Optional) A list of Kubernetes API server flags
# All flags can be found here https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver
#rke2_kube_apiserver_args: []

# Override default containerd snapshotter
rke2_snapshooter: overlayfs
```

## Inventory file example

This role relies on nodes distribution to `masters` and `workers` inventory groups. 
The RKE2 Kubernetes master/server nodes must belong to `masters` group and worker/agent nodes must be the members of `workers` group. Both groups has to be the children of `k8s_cluster` group.

```ini
[masters]
master-01 ansible_host=192.168.123.1 rke2_type=server
master-02 ansible_host=192.168.123.2 rke2_type=server
master-03 ansible_host=192.168.123.3 rke2_type=server

[workers]
worker-01 ansible_host=192.168.123.11 rke2_type=agent
worker-02 ansible_host=192.168.123.12 rke2_type=agent
worker-03 ansible_host=192.168.123.13 rke2_type=agent

[k8s_cluster:children]
masters
workers
```

## Playbook example

This playbook will deploy RKE2 to a single node acting as both server and agent.

```yaml
- name: Deploy RKE2
  hosts: node
  become: yes
  roles:
     - role: lablabs.rke2

```

This playbook will deploy RKE2 to a cluster with one server(master) and several agent(worker) nodes.

```yaml
- name: Deploy RKE2
  hosts: all
  become: yes
  roles:
     - role: lablabs.rke2

```

This playbook will deploy RKE2 to a cluster with HA server(master) control-plane and several  agent(worker) nodes. The server(master) nodes will be tainted so the workload will be distributed only on worker/agent nodes. The role will install also keepalived on the control-plane nodes and setup VIP address where the Kubernetes API will be reachable. it will also download the Kubernetes config file to the local machine.

```yaml
- name: Deploy RKE2
  hosts: all
  become: yes
  vars:
    rke2_ha_mode: true
    rke2_server_taint: true
    rke2_api_ip : 192.168.123.100
    rke2_download_kubeconf: true
  roles:
     - role: lablabs.rke2

```

## License

MIT

## Author Information

Created in 2021 by Labyrinth Labs
