import os
import time

from settings import settings
# from tqdm import tqdm

def ip_replace_last_octet(ip_addr, new_val):

    return '.'.join(ip_addr.split('.')[:-1]+[new_val])

def extract_iface_from_hostapd_conf(hostapd_conf_path):

    with open(hostapd_conf_path) as fd:
        for line in fd:
            if line.startswith('interface='):
                interface = line.strip().split('=')[1]
                return interface
    

def parse_boolean(raw_str):

    raw_str = raw_str.strip().lower()
    if raw_str == 'false':
        return False
    if raw_str == '0':
        return False
    if raw_str == 'no':
        return False
    return True

def sleep_bar(sleep_time, text=''):

    # sleep_time = int(sleep_time)
    #
    # print()

    time.sleep(sleep_time)
    if text:

        print(text)
        print()

    # interval = sleep_time % 1
    # if interval == 0:
    #     interval = 1
    #     iterations = sleep_time
    # else:
    #     iterations = sleep_time / interval
    #
    # for i in tqdm(list(range(iterations))):
    #     time.sleep(interval)
    #
    # print()


def am_i_rooot():
    print('[*] Checking for rootness...')
    if not os.geteuid()==0:
        sys.exit('[!] EAPMartello must be run as root: aborting.')

def create_work_folder():
    try:
        os.mkdir("/tmp/eapmartello")
    except FileExistsError:
        # it probably exists. But should check. TODO.
        pass

def extract_iface_from_hostapd_conf(hostapd_conf_path):
    with open(hostapd_conf_path) as fd:
        for line in fd:
            if line.startswith('interface='):
                interface = line.strip().split('=')[1]
                return interface

