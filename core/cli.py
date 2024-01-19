import argparse
import os
import sys

from settings import settings

# from cert_wizard import cert_utils

# Python3 FTW
from pathlib import Path

BASIC_OPTIONS = [
    'cert_wizard',
    'list_templates',
    'reap_creds',
    'mac_whitelist',
    'mac_blacklist',
    'ssid_whitelist',
    'ssid_blacklist',
    'hostile_portal',
    'debug',
    'interface',
    'essid',
    'bssid',
    'channel',
    'hw_mode',
    'cloaking',
    'auth',
    'karma',
    'mana',
    'loud',
    'name',
    'known_beacons',
    'channel_width',
    'auth_alg',
    'wpa_version',
    'known_ssids_file',
    'known_ssids',
    'negotiate',
]

ROGUE_AP_ATTACKS = [
    'reap_creds',
]

def set_options():


    parser = argparse.ArgumentParser()

    modes_group = parser.add_argument_group('Modes')
    modes_group_ = modes_group.add_mutually_exclusive_group()

    modes_group_.add_argument('--cert-wizard',
                              dest='cert_wizard',
                              choices=[
                                'create',
                                'import',
                                'interactive',
                                'list',
                                'dh',
                              ],
                              default=False,
                              nargs='?',
                              const='interactive',
                              help='Use this flag to run in Cert Wizard mode. '
                                   'Use "--cert-wizard create" to create '
                                   'a new certificate. Use "--cert-wizard '
                                   'interactive" or simply "--cert-wizard" '
                                   'to run Cert Wizard in interactive mode. '
                                   'Use "--cert-wizard import" to import '
                                   'a set of certificates into eaphammer\'s '
                                   'static configuration. Use "--cert-wizard '
                                   'list" to list all previously imported '
                                   'certs, as well as the active cert '
                                   'configuration. Use "--cert-wizard dh" '
                                   'to manually regenerate eaphammer\'s dh '
                                   'parameters.')

    modes_group_.add_argument('--creds', '--brad',
                              dest='reap_creds',
                              action='store_true',
                              help='Harvest EAP creds using evil twin attack')

    modes_group_.add_argument('--hostile-portal',
                              dest='hostile_portal',
                              action='store_true',
                              help='Force clients to connect '
                                   'to hostile portal')

    parser.add_argument('--manual-config',
                        dest='manual_config',
                        type=str,
                        default=None,
                        metavar='config_file',
                        help='Bypass eaphammer\'s hostapd '
                             'configuration manager and load '
                             'your own hostapd.conf file instead.')

    parser.add_argument('--save-config',
                        dest='save_config',
                        action='store_true',
                        default=None,
                        help='Save hostapd config file on exist.')

    parser.add_argument('--save-config-only',
                        dest='save_config_only',
                        action='store_true',
                        default=None,
                        help='Don\'t actually run anything. Instead, '
                             'just generate a hostapd config file using '
                             'user supplied parameters then exit.')

    parser.add_argument('--debug',
                        dest='debug',
                        action='store_true',
                        help='Enable debug output.')

    parser.add_argument('--advanced-help', '-hh',
                        dest='advanced_help',
                        action='store_true',
                        help='Show extended help options then exit.')


    access_point_group = parser.add_argument_group('Access Point')

    access_point_group.add_argument('--lhost',
                    dest='lhost',
                    type=str,
                    default='10.0.0.1',
                    required=False,
                    help='Your AP\'s IP address')

    access_point_group.add_argument('-i', '--interface',
                                    dest='interface',
                                    default=None,
                                    type=str,
                                    help='The phy interface on which '
                                         'to create the AP')

    access_point_group.add_argument('-e', '--essid',
                                    dest='essid',
                                    default=None,
                                    type=str,
                                    help='Specify access point ESSID')

    access_point_group.add_argument('-b', '--bssid',
                                    dest='bssid',
                                    default=None,
                                    type=str,
                                    help='Specify access point BSSID')

    access_point_group.add_argument('-c', '--channel',
                                    dest='channel',
                                    type=int,
                                    default=None,
                                    help='Specify access point channel '
                                         '(default: 1).')

    access_point_group.add_argument('--hw-mode',
                                    dest='hw_mode',
                                    type=str,
                                    default=None,
                                    help='Specify access point hardware mode '
                                         '(defaults: g for 2.4GHz channels, '
                                         'a for 5GHz channels).')

    access_point_group.add_argument('--cloaking',
                                    dest='cloaking',
                                    choices=['none', 'full', 'zeroes'],
                                    default=None,
                                    help='Send empty SSID in beacons and '
                                         'ignore probe request '
                                         'frames that do not specify '
                                         'full SSID (i.e. require '
                                         'stations to know SSID). '
                                         'Choices: [1. none - do '
                                         'not use SSID cloaking. ] '
                                         '[2. full - Send empty string'
                                         ' in beacon and ignore probe '
                                         'requests for broadcast '
                                         'SSID ] [3. zeroes - Replace '
                                         'all characters in SSID '
                                         'with ASCII 0 and ignore '
                                         'probe requests for '
                                         'broadcast SSID.]')

    access_point_group.add_argument('--auth',
                                    dest='auth',
                                    type=str,
                                    choices=[
                                        'open',
                                        'wpa-psk',
                                        'wpa-eap',
                                        'owe',
                                        'owe-transition',
                                        'owe-psk',
                                    ],
                                    default=None,
                                    help='Specify authentication mechanism '
                                         '(hostile and captive portal '
                                         'default: open )'
                                         '(creds default: wpa-eap).')

    access_point_group.add_argument('--karma', '--mana',
                                    dest='karma',
                                    action='store_true',
                                    help='Enable karma.')

    access_point_group.add_argument('--mac-whitelist',
                                    dest='mac_whitelist',
                                    type=str,
                                    default=None,
                                    help='Enable MAC address whitelisting '
                                         'and specify path to whitelist '
                                         'file.')

    access_point_group.add_argument('--mac-blacklist',
                                    dest='mac_blacklist',
                                    type=str,
                                    default=None,
                                    help='Enable MAC address blacklisting '
                                         'and specify path to blacklist '
                                         'file.')

    access_point_group.add_argument('--ssid-whitelist',
                                    dest='ssid_whitelist',
                                    type=str,
                                    default=None,
                                    help='Enable MAC address whitelisting '
                                         'and specify path to whitelist '
                                         'file.')

    access_point_group.add_argument('--ssid-blacklist',
                                    dest='ssid_blacklist',
                                    type=str,
                                    default=None,
                                    help='Enable MAC address blacklisting '
                                         'and specify path to blacklist '
                                         'file.')

    karma_group = parser.add_argument_group('Karma Options')

    karma_group.add_argument('--loud', '--singe',
                                    dest='loud',
                                    action='store_true',
                                    help='Enable loud karma mode.')

    karma_group.add_argument('--known-beacons',
                                    dest='known_beacons',
                                    action='store_true',
                                    help='Enable persistent known beacons attack.')

    default_ssid_list = os.path.join(
        settings.dict['paths']['directories']['wordlists'],
        settings.dict['core']['eaphammer']['general']['default_ssid_list'],
    )
    karma_group.add_argument('--known-ssids-file',
                           dest='known_ssids_file',
                           default=None,
                           type=str,
                           help='Specify the wordlist to use with '
                                'the --known-beacons features.')

    karma_group.add_argument('--known-ssids',
                           dest='known_ssids',
                           nargs='+',
                           default=None,
                           type=str,
                           help='Specify known ssids via the CLI')

    ap_advanced_subgroup = parser.add_argument_group('AP Advanced Options')

    ap_advanced_subgroup.add_argument('--wmm',
                                      dest='wmm',
                                      action='store_true',
                                      help='Enable wmm (further configuration '
                                           'of wmm performed in hostapd.ini)')

    ap_advanced_subgroup.add_argument('--driver',
                                      dest='driver',
                                      default=None,
                                      type=str,
                                      help='Specify driver.')

    ap_advanced_subgroup.add_argument('--beacon-interval',
                                      dest='beacon_interval',
                                      default=None,
                                      type=int,
                                      metavar='TUs',
                                      help='Send beacon packets every n '
                                           'Time Units (TUs). '
                                           'A single TU is equal to '
                                           '1024 microseconds. '
                                           '(default: 100)')

    ap_advanced_subgroup.add_argument('--dtim-period',
                                      dest='dtim_period',
                                      default=None,
                                      type=int,
                                      metavar='n',
                                      help='Transmit broadcast frames after '
                                           'every n beacons, '
                                           'where n is an integer between '
                                           '1 and 255. (default: 1)')

    ap_advanced_subgroup.add_argument('--max-num-stations',
                                      dest='max_num_stations',
                                      default=None,
                                      type=int,
                                      help='The maximum number of '
                                           'stations that can '
                                           'connect to the AP at '
                                           'any one time. (default: 255)')

    ap_advanced_subgroup.add_argument('--rts-threshold',
                                      dest='rts_threshold',
                                      default=None,
                                      type=int,
                                      metavar='OCTETS',
                                      help='Sets the RTS threshold in '
                                           'octets. (default: 2347)')

    ap_advanced_subgroup.add_argument('--fragm-threshold',
                                      dest='fragm_threshold',
                                      default=None,
                                      type=int,
                                      metavar='OCTETS',
                                      help='Sets the fragmentation '
                                           'threshold in octets. '
                                           '(default: 2346)')

    hwm80211n_subgroup = parser.add_argument_group(
                                    '802.11n Options',
                                    'Used when --hw-mode is set to "n"',
    )

    hwm80211n_subgroup.add_argument('--channel-width',
                                    dest='channel_width',
                                    type=int,
                                    choices=[20,40],
                                    default=None,
                                    metavar='MGhz',
                                    help='Set the channel width '
                                         'in MGHz (single 20 MGHz '
                                         'spatial stream or two 20 '
                                         'MGHz spatial streams '
                                         'totalling 40 MGHz). (default: 20)')

    hwm80211n_advanced_subgroup = parser.add_argument_group(
                                        '802.11n Advanced Options',
    )

    hwm80211n_advanced_subgroup.add_argument('--smps',
                                             dest='smps',
                                             type=str,
                                             choices=['off','dynamic','static'],
                                             default=None,
                                             help='Spatial Multiplexing '
                                                  '(SM) Power Save')

    hwm80211n_advanced_subgroup.add_argument('--ht40',
                                             dest='ht40',
                                             type=str,
                                             choices=['plus', 'minus', 'auto'],
                                             default=None,
                                             help='Specifies whether the '
                                                  'secondary channel should be '
                                                  'higher (plus) or lower '
                                                  '(minus) than the primary '
                                                  'channel. (default: auto)')

    hwm80211n_advanced_subgroup.add_argument('--max-spatial-streams',
                                             dest='max_spatial_streams',
                                             type=int,
                                             choices=[1,2,3],
                                             default=None,
                                             help='Specifies maximum '
                                                  'number of spatial streams. '
                                                  '(default: 2)')

    hwm80211n_advanced_subgroup.add_argument('--obss-interval',
                                             dest='obss_interval',
                                             type=None,
                                             default=None,
                                             help='Look this up if you don\'t '
                                                  'know what it does. You '
                                                  'probably don\'t need '
                                                  'it. (default: 0)')

    hwm80211n_advanced_subgroup.add_argument('--greenfield',
                                             dest='greenfield',
                                             action='store_true',
                                             help='Enable greenfield mode.')

    hwm80211n_advanced_subgroup.add_argument('--ht-delayed-block-ack',
                                             dest='ht_delayed_block_ack',
                                             action='store_true',
                                             help='Use HT Delayed Block ACK.')

    hwm80211n_advanced_subgroup.add_argument('--short-gi',
                                             dest='short_gi',
                                             action='store_true',
                                             help='Enable short GI (20 or 40 '
                                                  'depending on channel width')

    hwm80211n_advanced_subgroup.add_argument('--lsig-txop-prot',
                                             dest='lsig_txop_prot',
                                             action='store_true',
                                             help='Enable L-SIG '
                                                  'TXOP Protection support.')

    hwm80211n_advanced_subgroup.add_argument('--require-ht',
                                             dest='require_ht',
                                             action='store_true',
                                             help='Reject associations from '
                                                  'clients that do '
                                                  'not support HT.')

    hwm80211n_advanced_subgroup.add_argument('--dsss-cck-40',
                                             dest='dsss_cck_40',
                                             action='store_true',
                                             help='Enable DSSS/CCK Mode in 40MHz.')

    hwm80211n_advanced_subgroup.add_argument('--disable-tx-stbc',
                                             dest='disable_tx_stbc',
                                             action='store_true',
                                             help='Disable TX-STBC.')

    hwm80211n_advanced_subgroup.add_argument('--ldpc',
                                             dest='ldpc',
                                             action='store_true',
                                             help='Enable LDPC Coding capability.')

    hwm80211n_advanced_subgroup.add_argument('--use-max-a-msdu-length',
                                             dest='use_max_a_msdu_length',
                                             action='store_true',
                                             help='Set A-MSDU length to '
                                                  'maximum allowable '
                                                  'value (7935 octets). '
                                                  'If not set, 3839 '
                                                  'octets are used.')

    eap_group = parser.add_argument_group(
                        'EAP Options',
                        'Only applicable if --auth wpa-eap is used',
    )

    eap_group.add_argument('--negotiate',
                           dest='negotiate',
                           choices=[
                                'balanced',
                                'speed',
                                'weakest',
                                'gtc-downgrade',
                                'manual',
                           ],
                           type=str,
                           default='balanced',
                           help='Specify EAP negotiation approach.')

    eap_group.add_argument('--eap-user-file',
                           dest='eap_user_file',
                           default=None,
                           type=str,
                           help=('Manually specify path to '
                                 'eap_user_file (instead of '
                                 'using EAPHammer\'s accounting '
                                 'system)'))

    eap_group.add_argument('--phase-1-methods',
                          dest='eap_methods_phase_1',
                          default='PEAP,TTLS,TLS,FAST',
                          type=str,
                          help=('Manually specify EAP phase 1 methods for '
                                'for wildcard user EAP negotiate.'))

    eap_group.add_argument('--phase-2-methods',
                          dest='eap_methods_phase_2',
                          default=('GTC,TTLS-PAP,MD5,TTLS-CHAP,'
                                   'TTLS-MSCHAP,MSCHAPV2,'
                                   'TTLS-MSCHAPV2,TTLS'),
                          type=str,
                          help=('Manually specify EAP phase 2 methods for '
                                'for wildcard user EAP negotiate.'))

    eap_group.add_argument('--peap-version',
                           dest='peap_version',
                           choices=[1, 2],
                           type=int,
                           default=None,
                           help='Specify EAP negotiation approach.')

    try:

        if '-hh' not in sys.argv and '--advanced-help' not in sys.argv:
            for a in parser._actions:
                if a.dest != 'help' and a.dest not in BASIC_OPTIONS:
                    a.help = argparse.SUPPRESS

        args = parser.parse_args()

        options = args.__dict__

        if options['advanced_help']:
            parser.print_help()
            sys.exit()

        if (options['cert_wizard'] is False and
            options['manual_config'] is None and
            options['advanced_help'] is False and
            options['interface'] is None):

            parser.print_usage()
            print()
            print('[!] Please specify a valid PHY', end=' ')
            print('interface using the --interface flag')
            sys.exit()

        if options['loud'] and not options['karma']:

            parser.print_usage()
            print()
            msg = ('[!] Cannot use --loud flag without --karma flag.')
            print(msg, end='')
            sys.exit()

        # sanity checks for known beacons attack
        if options['known_beacons']:

            if not options['karma']:

                parser.print_usage()
                print()
                msg = ('[!] Cannot use --known-beacons flag without --karma flag.')
                print(msg, end='')
                sys.exit()

            if options['known_ssids_file'] is None and \
                    options['known_ssids'] is None:

                parser.print_usage()
                print()
                msg = ('[!] Cannot use --known-beacons '
                        'without list of known SSIDS. '
                        'Please specify path to known SSIDS '
                        'file with the --known-ssids-file flag, '
                        'or provide a list of known SSIDS '
                        'using the --known-ssids flag.')
                print(msg, end='')
                sys.exit()
                
            if options['known_ssids_file'] is not None and \
                    options['known_ssids'] is not None:

                parser.print_usage()
                print()
                msg = ('[!] Cannot use --known-ssids-file '
                        'and --known-ssids flags simultaneously.')
                print(msg, end='')
                sys.exit()

            if options['known_ssids_file'] is not None and \
                not Path(options['known_ssids_file']).is_file():

                parser.print_usage()
                print()
                msg = ('[!] Specified known SSID file not found: {}'.format(options['known_ssids_file']))
                print(msg, end='')
                sys.exit()
                
        if options['mac_whitelist'] is not None and options['mac_blacklist'] is not None:

            parser.print_usage()
            print()
            msg = ('[!] Cannot use --mac-whitelist and '
                   '--mac-blacklist flags simultaneously.')
            print(msg, end='')
            sys.exit()

        if options['ssid_whitelist'] is not None and options['ssid_blacklist'] is not None:

            parser.print_usage()
            print()
            msg = ('[!] Cannot use --ssid-whitelist and '
                   '--ssid-blacklist flags simultaneously.')
            print(msg, end='')
            sys.exit()

        # these sanity checks probably needs to be moved somewhere else,
        # but whatever. fuckit shipit.
        if options['ssid_whitelist']:
            with open(options['ssid_whitelist']) as input_handle:
                for index,line in enumerate(input_handle):
                    ssid = line.strip()
                    if len(ssid) > 32:
                        parser.print_usage()
                        print()
                        msg = ('[!] In SSID whitelist file {} line {}: '
                               'Length of SSID {} is too long. SSIDS must '
                               'have a length of no more than 32 '  
                               'characters.'.format(options['ssid_whitelist'],
                                                index+1, ssid))
                        print(msg, end='')
                        sys.exit()

        if options['ssid_blacklist']:
            with open(options['ssid_blacklist']) as input_handle:
                for index,line in enumerate(input_handle):
                    ssid = line.strip()
                    if len(ssid) > 32:
                        parser.print_usage()
                        print()
                        msg = ('[!] In SSID blacklist file {} line {}: '
                               'Length of SSID {} is too long. SSIDS must '
                               'have a length of no more than 32 '  
                               'characters.'.format(options['ssid_blacklist'],
                                                index+1, ssid))
                        print(msg, end='')
                        sys.exit()


    except SystemExit:

        print()
        print('[!] Use -h or --help to display a list of basic options.')
        msg = ('[!] Use -hh or --advanced-help to '
               'display full list of extended options.')
        print(msg)
        print()

        raise

    if options['manual_config'] is not None:

        with open(options['manual_config']) as fd:

            for line in fd:
                if 'interface' in line:
                    options['interface'] = line.strip().split('=')[1]
        if options['interface'] is None:
            print()
            msg = ('[!] Please specify a valid PHY '
                   'interface in your config file.')
            print(msg)
            sys.exit()

    if options['negotiate'] == 'gtc-downgrade':
        options['negotiate'] = 'gtc_downgrade'

    return options
