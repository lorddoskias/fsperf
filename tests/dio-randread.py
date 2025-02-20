import sys
from PerfTest import FioTest
from utils import get_fstype,set_readpolicy,get_active_readpolicy,has_readpolicy
from utils import NotRunException

class DioRandread(FioTest):
    name = "diorandread"
    command = ("--name diorandread --direct=1 --size=1g --rw=randread "
               "--runtime=60 --iodepth=1024 --nrfiles=16 "
               "--numjobs=16 --group_reporting")

    def setup(self, config, section):
        device = config.get(section, 'device')

        if not get_fstype(device) == "btrfs":
            return

        if config.has_option(section, 'readpolicy'):
            policy = config.get(section, 'readpolicy')
            if not has_readpolicy(device):
                raise NotRunException("Kernel does not support readpolicy")

            set_readpolicy(config.get(section, 'device'), policy)
            policy = get_active_readpolicy(config.get(section, 'device'))
            print("\tReadpolicy is set to '{}'".format(policy))
