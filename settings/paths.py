import os
import json
import random
import string

from datetime import datetime

class OutputFile(object):

    def __init__(self, name='', ext='', length=32):
        datestring = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
        randstring = ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(length))
        self.str = ''
        if name != '':
            self.str += '%s-' % name
        self.str += '-'.join([datestring, randstring])
        if ext != '':
            self.str += '.%s' % ext.replace('.', '')

    def string(self):
        return self.str

    def __str__(self):
        return self.str

# define directories
ROOT_DIR = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONF_DIR = os.path.join(ROOT_DIR, 'settings')
SAVE_DIR = os.path.join(ROOT_DIR, 'saved-configs')
LOG_DIR = os.path.join(ROOT_DIR, 'output')
# RUN_DIR = os.path.join(ROOT_DIR, 'run')
RUN_DIR = '/var/run'
SCRIPT_DIR = os.path.join(ROOT_DIR, 'scripts')
DB_DIR = os.path.join(ROOT_DIR, 'db')
TMP_DIR = '/tmp/eapmartello'
WORDLIST_DIR = os.path.join(ROOT_DIR, 'wordlists')
LOCAL_DIR = os.path.join(ROOT_DIR, 'local')
HOSTAPD_DIR = os.path.join(LOCAL_DIR, 'hostapd-eaphammer', 'hostapd')
CERTS_DIR = os.path.join(ROOT_DIR, 'certs')
LOOT_DIR = os.path.join(ROOT_DIR, 'loot')
THIRDPARTY_DIR = os.path.join(ROOT_DIR, 'thirdparty')

# wpa handshake cpature file paths
#options['psk_capture_file']
output_file = OutputFile(name='wpa_handshake_capture', ext='hccapx').string()
PSK_CAPTURE_FILE = os.path.join(LOOT_DIR, output_file)

# openssl paths
OPENSSL_BIN = os.path.join(LOCAL_DIR, 'openssl/local/bin/openssl')

# hostapd paths
HOSTAPD_BIN = os.path.join(HOSTAPD_DIR, 'hostapd-eaphammer')
HOSTAPD_LIB = os.path.join(HOSTAPD_DIR, 'libhostapd-eaphammer.so')
HOSTAPD_LOG = os.path.join(LOG_DIR, 'hostapd-eaphammer.log')
# output_file = 'tmp/hostapd-control-interface' # fuckit
output_file = OutputFile(name='ctrl-iface', length=8).string()
HOSTAPD_CTRL_INTERFACE = os.path.join(RUN_DIR, output_file)

output_file = OutputFile(name='hostapd', ext='conf').string()
HOSTAPD_CONF = os.path.join(TMP_DIR, output_file)
HOSTAPD_SAVE = os.path.join(SAVE_DIR, output_file)
FIFO_PATH = os.path.join(TMP_DIR, OutputFile(ext='fifo').string())

#EAP_USER_FILE = os.path.join(DB_DIR, 'eaphammer.eap_user')
output_file = OutputFile(ext='eap_user').string()
EAP_USER_FILE = os.path.join(TMP_DIR, output_file)
#EAP_USER_HEADER = os.path.join(DB_DIR, 'eap_user_header.txt')
EAP_USER_HEADER = os.path.join(DB_DIR, 'eap_user.header')
PHASE1_ACCOUNTS = os.path.join(DB_DIR, 'phase1.accounts')
PHASE2_ACCOUNTS = os.path.join(DB_DIR, 'phase2.accounts')

# known ssids file
output_file = OutputFile(ext='known_ssids').string()
KNOWN_SSIDS_FILE = os.path.join(TMP_DIR, output_file)

# ACL Files
output_file = OutputFile(ext='accept').string()
HOSTAPD_MAC_WHITELIST = os.path.join(TMP_DIR, output_file)
output_file = OutputFile(ext='deny').string()
HOSTAPD_MAC_BLACKLIST = os.path.join(TMP_DIR, output_file)

output_file = OutputFile(ext='accept').string()
HOSTAPD_SSID_WHITELIST = os.path.join(TMP_DIR, output_file)
output_file = OutputFile(ext='deny').string()
HOSTAPD_SSID_BLACKLIST = os.path.join(TMP_DIR, output_file)

# cert paths
ACTIVE_FULL_CHAIN = os.path.join(CERTS_DIR, 'fullchain.pem')
DH_FILE = os.path.join(CERTS_DIR, 'dh')


paths = {
    'directories' : {
        'root' : ROOT_DIR,
        'conf' : CONF_DIR,
        'log' : LOG_DIR,
        'scripts' : SCRIPT_DIR,
        'db' : DB_DIR,
        'tmp' : TMP_DIR,
        'wordlists' : WORDLIST_DIR,
        'local' : LOCAL_DIR,
        'hostapd' : HOSTAPD_DIR,
        'certs' : CERTS_DIR,
        'saves' : SAVE_DIR,
    },
    'hostapd' : {
        'bin' : HOSTAPD_BIN,
        'lib' : HOSTAPD_LIB,
        'log' : HOSTAPD_LOG,
        'eap_user'  : EAP_USER_FILE,
        'eap_user_header'  : EAP_USER_HEADER,
        'phase1_accounts' : PHASE1_ACCOUNTS,
        'phase2_accounts' : PHASE2_ACCOUNTS,
        'fifo' : FIFO_PATH,
        'ctrl_interface' : HOSTAPD_CTRL_INTERFACE,
        'conf' : HOSTAPD_CONF,
        'save' : HOSTAPD_SAVE,
        'mac_whitelist' : HOSTAPD_MAC_WHITELIST,
        'mac_blacklist' : HOSTAPD_MAC_BLACKLIST,
        'ssid_whitelist' : HOSTAPD_SSID_WHITELIST,
        'ssid_blacklist' : HOSTAPD_SSID_BLACKLIST,
        'known_ssids' : KNOWN_SSIDS_FILE,
    },

    'certs' : {
        'dh' : DH_FILE,
        'active_full_chain' : ACTIVE_FULL_CHAIN,
    },

    'openssl' : {
        'bin' : OPENSSL_BIN,
    },
}

