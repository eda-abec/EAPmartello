# Eapmartello

Fork of Eaphammer.

My humble attempt to make Eaphammer less messy and to do only one thing that it does well - WPA Enterprise evil twin.

More text in progress.

## Setup Instructions
Run `make setup` and `make setup_certificates`.
Files in the dependencies folder can be safely deleted after setup, only the libhostapd-eaphammer.so is needed. Also openssl binary to generate certificates.

## Usage
`sudo python3 martello.py -i wlan0 -e evilSSID`

## Features

### Implemented
- less dependencies, do only WPA Enterprise evil twin
- current version (that is still compatible) of OpenSSL - 1.1.1.a


### TODO
- multiple SSIDs
