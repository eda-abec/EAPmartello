from . import utils
import subprocess
import time

class Interface(object):

    def __init__(self, interface):
        self.interface = interface

    def nm_off(self):
        print('[*] Reticulating radio frequency splines...')
        subprocess.check_call("nmcli device set %s managed no" % self.interface, shell=True)
        utils.sleep_bar(1, '[*] Using nmcli to tell NetworkManager not to manage %s...' % self.interface)
        print('[*] Success: %s no longer controlled by NetworkManager.' % self.interface)

    def nm_on(self):
        subprocess.check_call('nmcli device set %s managed yes' % self.interface, shell=True)
        utils.sleep_bar(1, '[*] Using nmcli to give NetworkManager control of %s...' % self.interface)
        print('[*] Success: %s is now managed by NetworkManager.' % self.interface)

    def set_ip_and_netmask(self, ip, netmask):
        subprocess.check_call('ifconfig %s %s netmask %s' % (self.interface, ip, netmask), shell=True)

    def __str__(self):
        return self.interface
