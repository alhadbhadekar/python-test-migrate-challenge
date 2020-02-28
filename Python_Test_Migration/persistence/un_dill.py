import dill
import sys
sys.path.append("..")
from provider.python_test_migration \
    import Credentials, MountPoint, Workload, MigrationTarget, Migration

def load_classes():
    with open('../tier_one/python_test_migration', 'rb') as f:
        credentials = dill.load(f)
        mountpoint = dill.load(f)
        workload = dill.load(f)
        migrationtarget = dill.load(f)
        migration = dill.load(f)
    #with open('basic', 'rb') as f:
    #    b = dill.load(f)
    #print('basic', b.x, b.y, b.z)