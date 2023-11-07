# What is VMware-DSM?
This is ansible playbook to deploy conviniently VMware Data Services Manager which  offers a data-as-a-service toolkit for on-demand provisioning and automated management of Microsoft SQL, PostgreSQL, and MySQL databases on vSphere environment. VMware Data Services Manager provides both a graphical user interface and a REST API in the toolkit, enabling both administrators and developers to get the most out of the service.
For more deatils about it, refer the following link. https://docs.vmware.com/en/VMware-Data-Services-Manager/1.5/data-services-manager/GUID-index.html

## Home network diagram for VMware DSM
It shows you home network diagram for VMware DSM
![alt text](https://github.com/rokmc756/VMware-DSM/blob/main/roles/provider/files/dsm_network_daigram.png)

## VMware DSM Architecutre in vSphere
It shows you internal VSM Arhicture in vSphere with Home network diagram
![alt text](https://github.com/rokmc756/VMware-DSM/blob/main/roles/provider/files/dsm_internal_architecture.png)

# Supported VMware vCenter and vSphere version
VMware vCenter 6.7.x, 7.x
VMware vSphere 6.7.x, 7.x

# Prerequisite
ansible

# Prepare ansible host to deploy or destroy VMware DSM
* MacOS
~~~
$ xcode-select --install
$ brew install ansible
$ brew install https://raw.githubusercontent.com/kadwanev/bigboybrew/master/Library/Formula/sshpass.rb
~~~

* Fedora/CentOS/RHEL
~~~
$ sudo yum install ansible
$ sudo yum install sshpass
~~~

# Download / configure / deploy or destory VMware DSM
$ git clone https://github.com/rokmc756/VMware-DSM

## Move base directory for VMware DSM
$ cd VMware-DSM

## Edit the password of ansilble host and target
$ vi Makefile
~~~
ANSIBLE_HOST_PASS="changeme"      # It should be changed with password of user in ansible host that gpfarmer would be run.
ANSIBLE_TARGET_PASS="changeme"    # It should be changed with password of sudo user in managed nodes that gpdb would be installed.
~~~

## Define ansible-hosts file
$ vi ansible-hosts
~~~
[all:vars]
ssh_key_filename="id_rsa"
remote_machine_username="root"
remote_machine_password="Changeme12!@"
ansible_python_interpreter=/usr/bin/python3

[esxi]
esxi7 ansible_ssh_host=192.168.0.101

[vcenter]
vcenter ansible_ssh_host=192.168.0.102 ansible_user=root ansible_password='Changeme12!@'

[provider]
dms-provider1 ansible_ssh_host=192.168.0.103

[agent]
dms-agent1 ansible_ssh_host=192.168.0.105

[minio]
rk9-minio ansible_ssh_host=192.168.0.98
~~~

## Defind all variables which would not that be changable for VMware DSM Provider & Agent VMs
$ vi group_vars/all.yml
~~~
# ansible_become_pass: "Changeme12!@"
ansible_become_pass: "Changeme12!@!@"

esxi:
  hostname: "esxi.jtest.pivotal.io"
  ipaddr: "192.168.0.101"
  username: "root"
  password: "Changeme12!@"
vcenter:
  hostname: "vcenter"
  ipaddr: "192.168.0.103"
  username: "administrator@vsphere.local"
  password: "Changeme12!@"
  vm_user: "root"
  vm_password: 'Changeme12!@'
  net_prefix: "24"
  net_gateway: '192.168.0.1'
  dns_servers: '192.168.0.199'
  domain: 'vcenter.jtest.pivotal.io'
  eth1_address: '192.168.219.102'
  eth1_network: '192.168.219.0'
  searchpath: 'jtest.pivotal.io'
  ## searchpath: ""
  datacenter: 'jDC01'
  cluster: 'jClu01'
  datastore: 'datastore1'
dsm:
  provider:
    vm_user: 'root'
    vm_password: 'Changeme12!@'
    eth0_ipaddr: '192.168.0.103'
    eth1_ipaddr: '192.168.219.103'
    net_prefix: '24'
    netmask: '255.255.255.0'
    gateway: '192.168.0.1'
    dns: '192.168.0.199'
    dns_servers: '192.168.0.199,8.8.8.8,168.126.63.1'
    domain: 'dsm-provider.jtest.pivotal.io'
    dsm_provider_size: '50G'
    ntp: "0.asia.pool.ntp.org"
    folder_name: ''
    vm_name: ''
  agent:
    vm_user: 'root'
    vm_password: 'Changeme12!@'
    eth0_ipaddr: '192.168.0.105'
    eth1_ipaddr: '192.168.219.105'
    prefix: '24'
    netmask: '255.255.255.0'
    gateway: '192.168.0.1'
    dns: '192.168.0.199'
    dns_servers: '192.168.0.199,8.8.8.8,168.126.63.1'
    ntp: "0.asia.pool.ntp.org"
    domain: 'dsm-agent.jtest.pivotal.io'
    searchpath: 'jtest.pivotal.io'
    folder_name: ''
    provider_username: 'jomoon@pivotal.io'
    provider_password: 'Changeme12!@'
~~~

## Define the name and size and local file location of VMware DSM Provider VM
$ vi roles/provider/vars/main.yml
~~~
# It makes confuse due to dms-provider is automatically generated by OVF
prefix_dsm_provider_vm_name: 'dms-provider'
dsm_provider_size: '50G'
dsm_provider_ova_file: 'roles/provider/files/dms-provider-va-1.5.0.2980-21842200.ova'
~~~

## Define the name and size and local file location of VMware DSM Agent VM
$ vi roles/agent/vars/main.yml
~~~
# It makes confuse due to dms-agent is automatically generated by OVF
prefix_dsm_agent_vm_name: 'dms-agent'
dsm_agent_size: '50G'
dsm_agent_ova_file: 'roles/agent/files/dms-agent-va-1.5.0.2797-21842199.ova'
~~~

## Configure roles and variables for deploying VMware DSM Provider & Agent VM
$ vi install-hosts.yml
~~~
---
- hosts: localhost
  gather_facts: true
  vars:
    deploy_ovf: true
    add_new_network_adapter: true
    configure_new_network: true
  roles:
    - provider
    - agent
~~~

## Run install-hosts.yml playbook
$ make install

## Configure roles and variables for destroying VMware DSM Provider & Agent VM
$ vi uninstall-hosts.yml
~~~
---
- hosts: localhost
  gather_facts: true
  vars:
    deploy_ovf: true
    add_new_network_adapter: true
    configure_new_network: true
  roles:
    - agent
    - provider
~~~

## Run uninstall-hosts.yml playbook
$ make uninstall



If you encounter the following error when running make install as above pyvmomi should be installed after removing pyvim.
Because this is a completely separate package (vim editor implemented in python). However, the name conflicts enough that the files get messed up.
~~~
An exception occurred during task execution. To see the full traceback, use -vvv. The error was: ImportError: No module named pyVim
~~~

The following step is what cleared it up.
~~~
$ pip3 uninstall pyvim
# may complain about manually added files.
$ cd /usr/local/lib/python3.7/site-packages
$ rm -rf pyvim
$ pip3 install --force pyvmomi
~~~

# Planning new roles and playbooks
- Uninstall DMS Provider and Agent - 2023-11-06 : Done
- Add settings for DMS nto vCenter
- Need to add Global Permission to users and assign roles to ReadOnly Users
- Need to use the vmware playbook provided by ansible-galaxy
-- https://github.com/ansible-collections/community.vmware
