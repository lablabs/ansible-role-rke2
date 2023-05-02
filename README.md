# RKE2 Ansible Role

[![Galaxy Quality](https://img.shields.io/ansible/quality/55229?style=flat&logo=ansible)](https://galaxy.ansible.com/lablabs/rke2)
[![Role version](https://img.shields.io/github/v/release/lablabs/ansible-role-rke2)](https://galaxy.ansible.com/lablabs/rke2)
[![Role downloads](https://img.shields.io/ansible/role/d/55229)](https://galaxy.ansible.com/lablabs/rke2)
[![GitHub Actions](https://github.com/lablabs/ansible-role-rke2/workflows/molecule%20test/badge.svg)](https://github.com/lablabs/ansible-role-rke2/actions)
[![License](https://img.shields.io/github/license/lablabs/ansible-role-rke2)](https://github.com/lablabs/ansible-role-rke2/blob/main/LICENSE)

[<img src="https://lablabs.io/static/ll-logo.png" width=350px>](https://lablabs.io/)

This Ansible role will deploy [RKE2](https://docs.rke2.io/) Kubernetes Cluster. RKE2 will be installed using the tarball method.

The Role can install the RKE2 in 3 modes:

- RKE2 single node

- RKE2 Cluster with one Server(Master) node and one or more Agent(Worker) nodes

- RKE2 Cluster with Server(Master) in High Availability mode and zero or more Agent(Worker) nodes. In HA mode you should have an odd number (three recommended) of server(master) nodes that will run etcd, the Kubernetes API (Keepalived VIP or Kube-VIP address), and other control plane services.

---
- Additionaly it is possible to install the RKE2 Cluster (all 3 modes) in Air-Gapped functionality with the use of local artifacts.

> It is possible to upgrade RKE2 by changing `rke2_version` variable and re-running the playbook with this role. During the upgrade process the RKE2 service on the nodes wil be restarted one by one. The Ansible Role will check if the node on which the service was restarted is in Ready state and only then procede with restarting service on another Kubernetes node.

## Requirements

* Ansible 2.10+

## Tested on

* Rocky Linux 8
* Ubuntu 20.04 LTS
* Ubuntu 22.04 LTS

## Role Variables

This is a copy of `defaults/main.yml`

```yaml
---
# The node type - server or agent
rke2_type: server

# Deploy the control plane in HA mode
rke2_ha_mode: false

# Install and configure Keepalived on Server nodes
# Can be disabled if you are using pre-configured Load Balancer
rke2_ha_mode_keepalived: true

# Install and configure kube-vip LB and VIP for cluster
# rke2_ha_mode_keepalived needs to be false
rke2_ha_mode_kubevip: false

# Kubernetes API and RKE2 registration IP address. The default Address is the IPv4 of the Server/Master node.
# In HA mode choose a static IP which will be set as VIP in keepalived.
# Or if the keepalived is disabled, use IP address of your LB.
rke2_api_ip: "{{ hostvars[groups[rke2_servers_group_name].0]['ansible_default_ipv4']['address'] }}"

# optional option for kubevip IP subnet
# rke2_api_cidr: 24

# optional option for kubevip
# rke2_interface: eth0

# optiononal option for kubevip load balancer IP range
# rke2_loadbalancer_ip_range: 192.168.1.50-192.168.1.100

# Install kubevip cloud provider if rke2_ha_mode_kubevip is true
rke2_kubevip_cloud_provider_enable: true

# Enable kube-vip to watch Services of type LoadBalancer
rke2_kubevip_svc_enable: true

# Add additional SANs in k8s API TLS cert
rke2_additional_sans: []

# API Server destination port
rke2_apiserver_dest_port: 6443

# Server nodes taints
rke2_server_node_taints: []
  # - 'CriticalAddonsOnly=true:NoExecute'

# Agent nodes taints
rke2_agent_node_taints: []

# Pre-shared secret token that other server or agent nodes will register with when connecting to the cluster
rke2_token: defaultSecret12345

# RKE2 version
rke2_version: v1.25.3+rke2r1

# URL to RKE2 repository
rke2_channel_url: https://update.rke2.io/v1-release/channels

# URL to RKE2 install bash script
# e.g. rancher chinase mirror http://rancher-mirror.rancher.cn/rke2/install.sh
rke2_install_bash_url: https://get.rke2.io

# Local data directory for RKE2
rke2_data_path: /var/lib/rancher/rke2

# Default URL to fetch artifacts
rke2_artifact_url: https://github.com/rancher/rke2/releases/download/

# Local path to store artifacts
rke2_artifact_path: /rke2/artifact

# Airgap required artifacts
rke2_artifact:
  - sha256sum-{{ rke2_architecture }}.txt
  - rke2.linux-{{ rke2_architecture }}.tar.gz
  - rke2-images.linux-{{ rke2_architecture }}.tar.zst

# Changes the deploy strategy to install based on local artifacts
rke2_airgap_mode: false

# Airgap implementation type - download, copy or exists
# - 'download' will fetch the artifacts on each node,
# - 'copy' will transfer local files in 'rke2_artifact' to the nodes,
# - 'exists' assumes 'rke2_artifact' files are already stored in 'rke2_artifact_path'
rke2_airgap_implementation: download

# Local source path where artifacts are stored
rke2_airgap_copy_sourcepath: local_artifacts

# Tarball images for additional components to be copied from rke2_airgap_copy_sourcepath to the nodes
# (File extensions in the list and on the real files must be retained)
rke2_airgap_copy_additional_tarballs: []

# Destination for airgap additional images tarballs ( see https://docs.rke2.io/install/airgap/#tarball-method )
rke2_tarball_images_path: "{{ rke2_data_path }}/agent/images"

# Architecture to be downloaded, currently there are releases for amd64 and s390x
rke2_architecture: amd64

# Destination directory for RKE2 installation script
rke2_install_script_dir: /var/tmp

# RKE2 channel
rke2_channel: stable

# Do not deploy packaged components and delete any deployed components
# Valid items: rke2-canal, rke2-coredns, rke2-ingress-nginx, rke2-metrics-server
rke2_disable:

# Option to disable kube-proxy
# disable_kube_proxy: true

# Path to custom manifests deployed during the RKE2 installation
# It is possible to use Jinja2 templating in the manifests
rke2_custom_manifests:

# Path to static pods deployed during the RKE2 installation
rke2_static_pods:

# Configure custom Containerd Registry
rke2_custom_registry_mirrors:
  - name:
    endpoint: {}
#   rewrite: '"^rancher/(.*)": "mirrorproject/rancher-images/$1"'

# Configure custom Containerd Registry additional configuration
# rke2_custom_registry_configs:
#   - endpoint:
#     config:

# Path to Container registry config file template
rke2_custom_registry_path: templates/registries.yaml.j2

# Path to RKE2 config file template
rke2_config: templates/config.yaml.j2

# Etcd snapshot source directory
rke2_etcd_snapshot_source_dir: etcd_snapshots

# Etcd snapshot file name.
# When the file name is defined, the etcd will be restored on initial deployment Ansible run.
# The etcd will be restored only during the initial run, so even if you will leave the the file name specified,
# the etcd will remain untouched during the next runs.
# You can either use this or set options in `rke2_etcd_snapshot_s3_options`
rke2_etcd_snapshot_file:

# Etcd snapshot location
rke2_etcd_snapshot_destination_dir: "{{ rke2_data_path }}/server/db/snapshots"

# Etcd snapshot s3 options
# Set either all these values or `rke2_etcd_snapshot_file` and `rke2_etcd_snapshot_source_dir`

# rke2_etcd_snapshot_s3_options:
  # s3_endpoint: "" # required
  # access_key: "" # required
  # secret_key: "" # required
  # bucket: "" # required
  # snapshot_name: "" # required.
  # skip_ssl_verify: false # optional
  # endpoint_ca: "" # optional. Can skip if using defaults
  # region: "" # optional - defaults to us-east-1
  # folder: "" # optional - defaults to top level of bucket
# Override default containerd snapshotter
rke2_snapshooter: overlayfs

# Deploy RKE2 with default CNI canal
rke2_cni: canal

# Validate system configuration against the selected benchmark
# (Supported value is "cis-1.23" or eventually "cis-1.6" if you are running RKE2 prior 1.25)
rke2_cis_profile: ""

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

# (Optional) Configure Proxy
# All flags can be found here https://github.com/rancher/rke2/blob/master/docs/advanced.md#configuring-an-http-proxy
# rke2_environment_options: []
#   - "option=value"
#   - "HTTP_PROXY=http://your-proxy.example.com:8888"

# Cordon, drain the node which is being upgraded. Uncordon the node once the RKE2 upgraded
rke2_drain_node_during_upgrade: false

# Wait for all pods to be ready after rke2-service restart during rolling restart.
rke2_wait_for_all_pods_to_be_ready: false

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

This playbook will deploy RKE2 to a cluster with one server(master) and several agent(worker) nodes in air-gapped mode. It will use Multus and Calico as CNI.

```yaml
- name: Deploy RKE2
  hosts: all
  become: yes
  vars:
    rke2_airgap_mode: true
    rke2_airgap_implementation: download
    rke2_cni:
      - multus
      - calico
    rke2_artifact:
      - sha256sum-{{ rke2_architecture }}.txt
      - rke2.linux-{{ rke2_architecture }}.tar.gz
      - rke2-images.linux-{{ rke2_architecture }}.tar.zst
    rke2_airgap_copy_additional_tarballs:
      - rke2-images-multus.linux-{{ rke2_architecture }}
      - rke2-images-calico.linux-{{ rke2_architecture }}
  roles:
     - role: lablabs.rke2

```

This playbook will deploy RKE2 to a cluster with HA server(master) control-plane and several agent(worker) nodes. The server(master) nodes will be tainted so the workload will be distributed only on worker(agent) nodes. The role will install also keepalived on the control-plane nodes and setup VIP address where the Kubernetes API will be reachable. it will also download the Kubernetes config file to the local machine.

```yaml
- name: Deploy RKE2
  hosts: all
  become: yes
  vars:
    rke2_ha_mode: true
    rke2_api_ip : 192.168.123.100
    rke2_download_kubeconf: true
    rke2_server_node_taints:
      - 'CriticalAddonsOnly=true:NoExecute'
  roles:
     - role: lablabs.rke2

```

## Having separate token for agent nodes

As per [server configuration documentation](https://docs.rke2.io/reference/server_config) it is possible to define an agent token, which will be used by agent nodes to connect to cluster, giving them less access to cluster than server nodes have.
Following modifications to above configuration would be necessary:
- remove `rke2_token` from global vars
- add to `group_vars/masters.yml`:
```yaml
rke2_token: defaultSecret12345
rke2_agent_token: agentSecret54321
```
- add to `group_vars/workers.yml`:
```yaml
rke2_token: agentSecret54321
```

While changing server token is problematic, agent token can be rotated at will, as long as servers and agents have the same value and the services
(`rke2-server` and `rke2-agent`, as appropriate) have been restarted to make sure the processes use the new value.

## Troubleshooting

### Playbook stuck while starting the RKE2 service on agents

If the playbook starts to hang at the `Start RKE2 service on the rest of the nodes` task and then fails at the `Wait for remaining nodes to be ready` task, you probably have some limitations on you nodes' network.

Please check the required *Inbound Rules for RKE2 Server Nodes* at the following link: <https://docs.rke2.io/install/requirements/#networking>.

## License

MIT

## Author Information

Created in 2021 by Labyrinth Labs
