#!/usr/bin/env python3
#
# Parses stdout of Eaphammer and outputs a clean file with creds


import sys

separator = "\t"


input_file = sys.argv[1]
logfile = open(input_file)

try:
    gtc_output_file = sys.argv[2]
except:
    gtc_output_file = 'gtc.csv'
try:
    mschapv2_output_file = sys.argv[3]
except:
    mschapv2_output_file = 'mschapv2.log'

gotHash = []
gotPlain = []

creds_mschapv2 = []
creds_plain = []


logfile = logfile.read().split("\n\n\n")
print("Loaded: {}".format(len(logfile)))


with open(gtc_output_file, 'w') as gtclog:
    with open(mschapv2_output_file, 'w') as mschapv2log:

        # list of entries. Each of few (arbitrary number) lines
        # and exactly one crenential
        for entry in logfile:
            lines = entry.strip().splitlines()

            for line in lines:
                if "username" in line:
                    username = line

            # duplicity handling
            if ("GTC" in entry or "eap-ttls/pap" in entry) and username not in gotPlain:
                gotPlain.append(username)

                for i in range(len(lines)):
                    lines[i] = lines[i].strip()
                cred = "\n".join(lines[:3])
                cred = cred.replace("GTC:", "").replace("eap-ttls/pap:", "")
                cred = cred.replace("\nusername:\t", separator)
                cred = cred.replace("\npassword:\t", separator)
                gtclog.write(cred + "\n")

            elif "mschapv2" in entry and username not in gotHash and username not in gotPlain:
                gotHash.append(username)
                mschapv2log.write("\n".join(lines) + "\n\n\n")


print(f"Unique plaintext: {len(gotPlain)}")
print(f"Unique MSCHAPv2: {len(gotHash)}")
