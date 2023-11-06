# What is VMware-DSM?
This is ansible playbook to deploy conviniently VMware Data Services Manager which  offers a data-as-a-service toolkit for on-demand provisioning and automated management of Microsoft SQL, PostgreSQL, and MySQL databases on vSphere environment. VMware Data Services Manager provides both a graphical user interface and a REST API in the toolkit, enabling both administrators and developers to get the most out of the service.
For more deatils about it, refer the following link. https://docs.vmware.com/en/VMware-Data-Services-Manager/1.5/data-services-manager/GUID-index.html



## VMware DSM Architecutre
![alt text](https://github.com/rokmc756/VMware-DSM/blob/main/roles/provider/files/dsm_network_daigram.png)
![alt text](https://github.com/rokmc756/VMware-DSMblob/main/roles/provider/files/dsm_internal_architecture.png)

# Supported VMware vCenter and vSphere version
VMware vCenter 6.7.x, 7.x
VMware vSphere 6.7.x, 7.x

# Prerequisite
ansible

# Prepare ansible host to run gpfarmer
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

# Download / configure / run gpfarmer
$ git clone https://github.com/rokmc756/VMware-DSM

$ cd VMware-DSM

$ vi Makefile
~~~
ANSIBLE_HOST_PASS="changeme"      # It should be changed with password of user in ansible host that gpfarmer would be run.
ANSIBLE_TARGET_PASS="changeme"    # It should be changed with password of sudo user in managed nodes that gpdb would be installed.
~~~

$ vi ansible-hosts
~~~
[all:vars]
ssh_key_filename="id_rsa"
remote_machine_username="root"
remote_machine_password="changeme"
ansible_python_interpreter=/usr/bin/python3

[esxi]
esxi7 ansible_ssh_host=192.168.0.101

[vcenter]
vcenter ansible_ssh_host=192.168.0.102
~~~

$ vi role/provider/var/main.yml
~~~
esxi_address: '192.168.0.101'
root_username: 'root'
root_password: 'Changeme12!@'
vcenter_hostname: 'vcenter.jtest.pivotal.io'
vcenter_username: 'administrator@vsphere.local'
vcenter_address: '192.168.0.102'
vcenter_password: 'Changeme12!@'
datastore_name: 'datastore1'
datacenter_name: 'jDC01'
cluster_name: 'jClu01'
resourcepool_name: ''
# resourcepool_name: 'Discovered virtual machine'
net_prefix: '24'
net_gateway: '192.168.0.1'
dns_servers: '192.168.0.199,168.126.63.1'
domain: 'dms-provider.jtest.pivotal.io'
searchpath: 'jtest.pivotal.io'
dsm_provider_size: '50G'
folder_name: ''
dsm_provider_ova_file: 'roles/provider/files/dms-provider-va-1.5.0.2980-21842200.ova'
~~~

$ vi role/agent/var/main.yml
~~~
esxi_address: '192.168.0.101'
root_username: 'root'
root_password: 'Changeme12!@'
vcenter_hostname: 'vcenter.jtest.pivotal.io'
vcenter_username: 'administrator@vsphere.local'
vcenter_address: '192.168.0.102'
vcenter_password: 'Changeme12!@'
datastore_name: 'datastore1'
datacenter_name: 'jDC01'
cluster_name: 'jClu01'
resourcepool_name: ''
# resourcepool_name: 'Discovered virtual machine'
net_prefix: '24'
net_gateway: '192.168.0.1'
dns_servers: '192.168.0.199,168.126.63.1'
domain: 'dms-agent.jtest.pivotal.io'
searchpath: 'jtest.pivotal.io'
dsm_agent_size: '50G'
folder_name: ''
dsm_agent_ova_file: 'roles/agent/files/dms-agent-va-1.5.0.2797-21842199.ova'
~~~

$ vi setup-host.yml
~~~
---
- hosts: localhost
  gather_facts: false
  vars:
    deploy_ovf: true
    add_new_network_adapter: true
    configure_new_network: true
  roles:
    - agent
      #    - provider
~~~

$ make install


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

# Planning
Uninstall DMS Provider and Agent
