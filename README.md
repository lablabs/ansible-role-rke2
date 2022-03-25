# RKE2 Ansible Role

[![Galaxy Quality](https://img.shields.io/ansible/quality/55229?style=flat&logo=ansible)](https://galaxy.ansible.com/lablabs/rke2)
[![Role version](https://img.shields.io/github/v/release/lablabs/ansible-role-rke2)](https://galaxy.ansible.com/lablabs/rke2)
[![Role downloads](https://img.shields.io/ansible/role/d/55229)](https://galaxy.ansible.com/lablabs/rke2)
[![GitHub Actions](https://github.com/lablabs/ansible-role-rke2/workflows/molecule%20test/badge.svg)](https://github.com/lablabs/ansible-role-rke2/actions)
[![License](https://img.shields.io/github/license/lablabs/ansible-role-rke2)](https://github.com/lablabs/ansible-role-rke2/blob/main/LICENSE)

[<img src="ll-logo.png">](https://lablabs.io/)

This Ansible role will deploy [RKE2](https://docs.rke2.io/) Kubernetes Cluster. RKE2 will be installed using the tarball method.

The Role can install the RKE2 in 4 modes:

- RKE2 single node

- RKE2 Cluster with one Server(Master) node and one or more Agent(Worker) nodes

- RKE2 Cluster using Air-Gapped functionality with the use of artifacts

- RKE2 Cluster with Server(Master) in High Availability mode and zero or more Agent(Worker) nodes. In HA mode you should have an odd number (three recommended) of server(master) nodes that will run etcd, the Kubernetes API (Keepalived VIP address), and other control plane services.

## Requirements

* Ansible 2.10+

## Tested on

* Rocky Linux 8
* Ubuntu 20.04 LTS

## Role Variables

This is a copy of `defaults/main.yml`

```yaml
---

# The node type - server or agent
rke_type: server

# Deploy the control plane in HA mode
rke2_ha_mode: false

# Install and configure Keepalived on Server nodes
# Can be disabled if you are using pre-configured Load Blancer
rke2_ha_mode_keepalived: true

# Kubernetes API and RKE2 registration IP address. The default Address is the IPv4 of the Server/Master node.
# In HA mode choose a static IP which will be set as VIP in keepalived.
# Or if the keepalived is disabled, use IP address of your LB.
rke2_api_ip: "{{ hostvars[groups[rke2_servers_group_name].0]['ansible_default_ipv4']['address'] }}"

# Add additional SANs in k8s API TLS cert
rke2_additional_sans: []

# API Server destination port
rke2_apiserver_dest_port: 6443

# If false, server node(s) will be schedulable and thus your workloads can get launched on them
rke2_server_taint: false

# Pre-shared secret token that other server or agent nodes will register with when connecting to the cluster
rke2_token: defaultSecret12345

# RKE2 version
rke2_version: v1.22.6+rke2r1

# URL to RKE2 repository
rke2_channel_url: https://update.rke2.io/v1-release/channels

# URL to RKE2 install bash script
# e.g. rancher chinase mirror http://rancher-mirror.rancher.cn/rke2/install.sh
rke2_install_bash_url: https://get.rke2.io

# Destination directory for RKE2 installation script
rke2_install_script_dir: /var/tmp

# RKE2 channel
rke2_channel: stable

# Do not deploy packaged components and delete any deployed components
# Valid items: rke2-canal, rke2-coredns, rke2-ingress-nginx, rke2-kube-proxy, rke2-metrics-server
rke2_disable:

# Path to custom manifests deployed during the RKE2 installation
rke2_custom_manifests:

# Path to static pods deployed during the RKE2 installation
rke2_static_pods:

# Configure custom Containerd Registry
rke2_custom_registry_mirrors:
  - name:
    endpoint: {}

# Path to Container registry config file template
rke2_custom_registry_path: templates/registries.yaml.j2

# Path to RKE2 config file template
rke2_config: templates/config.yaml.j2

# Override default containerd snapshotter
rke2_snapshooter: overlayfs

# Deploy RKE2 with default CNI canal
rke2_cni: canal

# Download Kubernetes config file to the Ansible controller
rke2_download_kubeconf: false

# Name of the Kubernetes config file will be downloaded to the Ansible controller
rke2_download_kubeconf_file_name: rke2.yaml

# Destination directory where the Kubernetes config file will be downloaded to the Ansible controller
rke2_download_kubeconf_path: /tmp

# Default Ansible Inventory Group name for RKE2 cluster
rke2_cluster_group_name: k8s_cluster

# Default Ansible Inventory Group name for RKE2 Servers
rke2_servers_group_name: masters

# Default Ansible Inventory Group name for RKE2 Agents
rke2_agents_group_name: workers

# (Optional) A list of Kubernetes API server flags
# All flags can be found here https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver
# rke2_kube_apiserver_args: []

# (Optional) List of Node labels
# k8s_node_label: []

# (Optional) Additional RKE2 server configuration options
# You could find the flags at https://docs.rke2.io/install/install_options/install_options/#configuring-rke2-server-nodes
# rke2_server_options:
#   - "option: value"

# (Optional) Additional RKE2 agent configuration options
# You could find the flags at https://docs.rke2.io/install/install_options/install_options/#configuring-linux-rke2-agent-nodes
# rke2_agent_options:
#   - "option: value"

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

This playbook will deploy RKE2 to a cluster with one server(master) and several agent(worker) nodes in air-gapped mode. This works from downloading artifacts. When the RKE2 script installs, it will use the artifacts instead of using online resources. 

```yaml
- name: Deploy RKE2
  hosts: all
  become: yes
  vars:
    rke2_airgap_mode: true
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
