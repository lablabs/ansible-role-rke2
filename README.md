# RKE2 Ansible Role

[![Galaxy Quality](https://img.shields.io/ansible/quality/XXXXX?style=flat&logo=ansible)](https://galaxy.ansible.com/lablabs/XXXXX)
[![Role version](https://img.shields.io/github/v/release/lablabs/ansible-role-rke2)](https://galaxy.ansible.com/lablabs/XXXXX)
[![Role downloads](https://img.shields.io/ansible/role/d/XXXXX)](https://galaxy.ansible.com/lablabs/XXXXX)
[![GitHub Actions](https://github.com/lablabs/ansible-role-rke2/workflows/molecule%20test/badge.svg?branch=main)](https://github.com/lablabs/ansible-role-rke2/actions)
[![License](https://img.shields.io/github/license/lablabs/ansible-role-rke2)](https://github.com/lablabs/ansible-role-rke2/blob/main/LICENSE)

[<img src="ll-logo.png">](https://lablabs.io/)

This Ansible role will deploy RKE2 Kubernetes Cluster. RKE2 will be installed using the tarball method.  

The Role can install the RKE2 in 3 modes.

- RKE2 single node

- RKE2 Cluster with one Server/Master node and zero or moder agent/worker nodes

- RKE2 Cluster with Server/Master High Availability mode and one or moder agent/worker nodes. In HA mode you should have an odd number (three recommended) of server/master nodes that will run etcd, the Kubernetes API, and other control plane services.

Also you can choose to taint the server/master node(s) to not to shchetule the workload on them.

## Requirements

* Ansible 2.10+

## Tested on

* Ubuntu 20.04 TLS

## Role Variables

This is a copy of `defaults/main.yml`

```yaml
# The node type - server or agent
rke2_type: server

# Deploy the cluster in HA mode
rke2_ha_mode: false

# RKE2 version
rke2_version: v1.20.4+rke2r1

# URL to RKE2 repository
rke2_channel_url: https://update.rke2.io/v1-release/channels

# RKE2 channel
rke2_channel: stable

# RKE2 installation method (tar or rpm)
rke2_method: tar

# RKE2 Kubernetes API IP address. The default Address is the IPv4 of the Server/Master node.
# In HA mode choose the a static IP which will be set as VIP in keepalived.
rke2_api_ip: "{{ hostvars[groups.masters.0]['ansible_default_ipv4']['address'] }} "

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

# API Server destination port
rke2_apiserver_dest_port: 6443

# Override default containerd snapshotter
rke2_snapshooter: overlayfs

# If false, server node(s) will be schedulable and thus your workloads can get launched on them
rke2_server_taint: false

# Pre-shared secret token that other server or agent nodes will register with when connecting to the cluster
rke2_token: defaultSecret12345
```

## Inventory example


## Playbook example

- name: Deploy RKE2
  hosts: all
  become: yes
  roles:
     - role: lablabs.rke2

...

## License

MIT

## Author Information

Created in 2021 by Labyrinth Labs
