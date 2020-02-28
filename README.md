# Instructions

## Python Test Migrate Challenge
A Python package to migrate cloud data

## GitHub Link
https://github.com/alhadbhadekar/python-test-migrate-challenge
## Installation
Use the package manager [pip] (https://pip.pypa.io/en/stable/) to install Python-Test-Migration-Challenge

## Command to Install
```bash
pip install Python-Test-Migration-Challenge
```

## Project Structure
<pre>
Root level package\
Provider\
|__Provider Classes serving for object Creation, backend structing\
Service\
|__Service Layer for business logic incorporation, calling backend Provider classes only through Service Layer, contains list of functions\
Tier_one\
|__Customer facing code to access Service Layer fucntions for writing Migration logics\
Persistence\
|__Modules to help store Classes in filesystems\
test\
|__Provider\
   |__Unit Test cases for Provider Layer\
|__Service\
   |__Unit Test cases for Service Layer
</pre> 







## Usage

#### Example 1: Tier one Layer to do migration

```python
#!/usr/bin/python
from Python_Test_Migration.service.app_service import *
from Python_Test_Migration.provider.constant import IP_ADDRESS
from Python_Test_Migration.persistence.make_dill import dump_classes
from Python_Test_Migration.persistence.un_dill import load_classes
import os


# Loading persistent classes
if os.stat("python_test_migration").st_size != 0:
    load_classes()

# List of sources
sources = []


# Creates credentials object for source 1
ipaddress1 = IP_ADDRESS('1.1.1.1')
credentials1 = credentials_create('test', 'password', ipaddress1)

# Creates credentials object for source 2
ipaddress2 = IP_ADDRESS('2.2.2.2')
credentials2 = credentials_create('test2', 'password', ipaddress2)

# Create Source Mount points for target source 1
mountpoint1 = mountpoint_create('C:\\', 25)
mountpoint2 = mountpoint_create('D:\\', 25)
mountpoint3 = mountpoint_create('E:\\', 25)


# Create Source Mount points for target source 2
mountpoint4 = mountpoint_create('C:\\', 25)
mountpoint5 = mountpoint_create('N:\\', 25)


# Create Mountpoint list for source1
mountpoint_list1 = mountpoints_list(mountpoint1, mountpoint2, mountpoint3)

# Create Mountpoint list for source2
mountpoint_list2 = mountpoints_list(mountpoint4, mountpoint5)


# Create Workload for source 1
source1 = workload_create(credentials1, mountpoint_list1)
sources.append(source1)
# Create Workload for source 2
source2 = workload_create(credentials2, mountpoint_list2)
sources.append(source2)


# Create Target VM
cloud_type = 'aws'
ipaddress_cloud = IP_ADDRESS('3.3.3.3')
creds_cloud = Credentials('mukul', '234234', ipaddress_cloud.get_ipaddress())
cloud_workload = Workload(creds_cloud)

targetVM = migrationTarget_Create(cloud_type,
                                  creds_cloud,
                                  cloud_workload)
if targetVM.cloudtype == 'Not Supported':
    sys.exit()


# Run Migration
# Check for constrains i.e. no source has same IP address and and ip address remains same during workload
# Above checks are being added to Service Layer Migration function

# Created selected mount types
selected_mountpoint = mountpoint_create('C:\\', 25)
selected_mountpoint_list = [selected_mountpoint.get_mountPoint_instances()]


run_migration = migration(selected_mountpoint_list,
                          source1, targetVM,
                          ipaddress1, sources, mountpoint_list1)

print(run_migration)
# Saving classes to filesystem
dump_classes()
```
#### Example 1: Service Layers functions available to call Provider Classes

```python
#!/usr/bin/python
import sys
sys.path.append("..")
from provider.python_test_migration \
    import Credentials, MountPoint, Workload, MigrationTarget, Migration


def credentials_create(username, password, ipaddress):
    """Service Layer to Create Credentials"""
    credentials = Credentials(username, password, ipaddress.get_ipaddress())
    return credentials


def credentials_get(credentials):
    """Service Layer to get credentials"""
    return credentials.get_Credentials()


def mountpoint_create(name, size):
    """Service Layer to create mountpoint"""
    mountpoint = MountPoint(name, size)
    return mountpoint


def mountpoint_get(mountpoint):
    """Service Layer to get Mountpoint details"""
    return mountpoint.get_mountPoint_instances()


def mountpoints_list(*args):
    """Service Layer to get mountpoint list"""
    mountpoints_list = []
    for instance in args:
        mountpoints_list.append(instance.get_mountPoint_instances())
    return mountpoints_list


def workload_create(creds, MountPoint):
    """Service Layer to create workload"""
    source = Workload(creds, MountPoint)
    return source


def workload_get(workload):
    """Service Layer to get workload details"""
    workload = workload.get_workload()
    return workload


def constrains(source, ipaddress):
    """Service Layer to check constrains"""
    return source.constrains(ipaddress.get_ipaddress())


def check_duplicate_ip(sources):
    """Service Layer to check sources from duplicate IP addresses"""
    sources_ips = []
    for instance in sources:
        sources_ips.append(instance.get_workload()['domain'])
    return sources[0].checksourceip(sources_ips)


def migrationTarget_Create(cloud_type, creds_cloud, cloud_workload):
    """Service Layer to create Migration target"""
    targetVM = MigrationTarget(cloud_type, creds_cloud, cloud_workload)
    return targetVM


def migrationTarget_get(targerVM):
    """Service Layer to get Migration Target details"""
    return targerVM.get_Migration_Target()


def check_Mounts(selected_mountpoint_list, mountpoint_list1):
    """Service Layer to check mounts if selected mount is present in provided mountpoints or no"""
    selected_mountpoint = []
    mountpoints_provided = []
    for item in selected_mountpoint_list:
        selected_mountpoint.append(item['mount_name'])
    for item in mountpoint_list1:
        mountpoints_provided.append(item['mount_name'])

    for i in selected_mountpoint:
        for j in mountpoints_provided:
            if i == j:
                return {
                    'key': 'success',
                    'message': 'Selected Mount type present in MountTypes provided'
                }
            else:
                return {
                    'key': 'error',
                    'message': 'Selected Mount type not present in MountTypes provided'
                }


def migration(selected_mountpoint, source,
              targetVM, ipaddress,
              sources, mountpoint_list1):
    """Service Layer to run migrations"""
    check_ipchanged = constrains(source, ipaddress)
    if check_ipchanged['key'] == 'error':
        return {
            'key': 'error',
            'message': check_ipchanged['message'],
            'migration_State': 'error'
        }

    check_mul_ips = check_duplicate_ip(sources)
    if check_mul_ips['key'] == 'error':
        return {
            'key': 'error',
            'message': check_mul_ips['message'],
            'migration_State': 'error'
        }

    check_mount = check_Mounts(selected_mountpoint, mountpoint_list1)
    if check_mount['key'] == 'error':
        return {
            'key': 'error',
            'message': check_mount['message'],
            'migration_State': 'error'
        }

    run_migration = Migration(selected_mountpoint, source, targetVM)
    status = run_migration.run(source, targetVM)
    return status
```
