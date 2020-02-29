# Instructions

## Python Test Migrate Challenge
A Python package to migrate cloud data

## GitHub Link
https://github.com/alhadbhadekar/python-test-migrate-challenge
## Installation
Use the package manager [pip] (https://pip.pypa.io/en/stable/) to install Python-Test-Migration-Challenge

## Command to Install
pip package Link: https://pypi.org/project/Python-Test-Migration-Challenge/1.0.2/
```bash
pip install Python-Test-Migration-Challenge==1.0.2
```

## Project Structure
<pre>
Python_Test_Migration (Root folder)\
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

# Print migration details
print(run_migration)
# Saving classes to filesystem
dump_classes()

```
#### Example 1: Service Layers functions available to call Provider Classes

```python
#!/usr/bin/python
from Python_Test_Migration.provider.python_test_migration \
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

#### Example 3: Provider Layer Classes

```python
#!/usr/bin/python
import time
import copy

class Credentials:
    """Class to create Credentials Objects"""

    def __init__(self, username=None, password=None, domain=None):
        """Init method for initializing variables"""
        self.username = username
        self.password = password
        self.domain = domain

    def get_Credentials(self):
        """Method to get credentials"""
        return {'username': self.username,
                'password': self.password,
                'domain': self.domain}


class MountPoint:
    """Class to create MountPoint Object"""

    def __init__(self, mount_point_name=None, size=None):
        """Init method to initialize MountPoint object"""
        self.mount_point_name = mount_point_name
        self.size = size

    def get_mountPoint_instances(self):
        """Method to get MountPoint instances with size"""
        return {
            'mount_name': self.mount_point_name,
            'size': self.size
        }


class Workload(object):
    """Class to create workload Object"""

    def __init__(self, credentials=None, mountpoint=None):
        """Init method to initialize Workload Object"""
        self.Credentials = credentials
        self.storage = []
        if mountpoint is not None:
            for instance in mountpoint:
                self.storage.append(instance)

    def constrains(self, ipaddress=None):
        """Method to identify if there is an IP address changed over Workload"""
        username = self.Credentials.username
        password = self.Credentials.password
        domain = self.Credentials.domain
        storage = self.storage
        if domain != ipaddress:
            return {'key': 'error',
                    'message': 'IP address changed'}

        if username is None or password is None or domain is None:
            return {'key': 'error',
                    'message': 'Either IP address or password or domain is None'}
        return {'key': 'success',
                'message': 'Constrains passed'}

    def checksourceip(self, source_ips):
        """Method to check if there are multiple sources with same IP address"""

        if len(source_ips) != len(set(source_ips)):
            return {'key': 'error',
                    'message': 'Duplicate IP Addresses exist'}
        return {'key': 'success',
                'message': 'All Sources have separate IP\'s'}

    def get_credentials(self):
        """Method to get credentials"""
        return {
            'username': self.Credentials.username,
            'password': self.Credentials.password
        }

    def get_workload(self):
        """Method to get workload details"""
        return {
            'username': self.Credentials.username,
            'password': self.Credentials.password,
            'domain': self.Credentials.domain,
            'mount_point': self.storage
        }


class MigrationTarget(object):
    """Class to create MigrationTarget object"""

    def __init__(self, cloudtype=None, credentials=None, workload=None):
        """Init method to initialize MigrationTarget object"""
        self.cloudtype = cloudtype
        self.Credentials = credentials
        self.Workload = workload

        if self.cloudtype != 'aws':
            if self.cloudtype != 'azure':
                if self.cloudtype != 'vsphere':
                    if self.cloudtype != 'vcloud':
                        self.cloudtype = 'Not Supported'

    def get_Migration_Target(self):
        """Method to get MigrationTarget Details"""
        storage = self.Workload.storage
        return {
            'cloud_type': self.cloudtype, \
            'username': self.Credentials.username, \
            'password': self.Credentials.password, \
            'domain': self.Credentials.domain, \
            'mountpoint': storage}


class Migration(object):
    """Class to create Migration object"""

    def __init__(self, mountpoint=None, sourceWorkload=None, targetMigrationTarget=None):
        """Init method for initializing Migration object"""
        self.mountpoint = mountpoint
        self.sourceWorkload = sourceWorkload
        self.targetMigrationTarget = targetMigrationTarget
        self.migration_State = 'not_started'

    def run(self, sourceWorkload=None, targetMigrationTarget=None):
        """run method to start migration"""
        time.sleep(1)

        selected_mountpoints = []
        #print(len(self.mountpoint))
        for i in range(0, len(self.mountpoint)):
            selected_mountpoints.append(self.mountpoint[i]['mount_name'])

        # Checking if C:\\ is allowed to migrate
        for directory in selected_mountpoints:
            if 'C:\\' == directory:
                allowed = True
                break
            else:
                allowed = False

        migration_State = 'not_started'

        if allowed:
            try:
                migration_State = 'running'

                # Copying source to TargetVM for migration
                targetMigrationTarget = copy.copy(sourceWorkload)

                # Logic to make sure target only has selected mountpoints
                credentials = Credentials(targetMigrationTarget.get_credentials()['username'],
                                          targetMigrationTarget.get_credentials()['password'])

                targetMigrationTarget = Workload(credentials, self.mountpoint)
                migration_State = 'success'
                return {'key': 'success',
                        'message': 'Migration successfully completed',
                        'migration_State': migration_State}
            except:
                migration_State = 'error'
                return {'key': 'error',
                        'message': 'Error happened during migration',
                        'migration_State': migration_State}

        else:
            migration_State = 'error'
            return {'key': 'error',
                    'message': 'C:\\ not allowed.',
                    'migration_State': migration_State}

```
