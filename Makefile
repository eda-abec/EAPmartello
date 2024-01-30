# eapmartello
# 01/2024

setup:
	cd dependencies && tar -xf openssl-1.1.1w.tar.gz
	cd dependencies && mv openssl-1.1.1w openssl
	cd dependencies/openssl && sh config enable-ssl2 enable-ssl3 enable-ssl3-method enable-des enable-rc4 enable-weak-ssl-ciphers
	cd dependencies/openssl && make

	cd dependencies && tar -xf hostapd-eaphammer.tar.gz
	cp dependencies/hostapd_config dependencies/hostapd-eaphammer/hostapd/.config
	cd dependencies/hostapd-eaphammer/hostapd && make hostapd-eaphammer_lib
	mv dependencies/hostapd-eaphammer/hostapd/libhostapd-eaphammer.so .

setup_certificates:
	mkdir certs
	dependencies/openssl/apps/openssl dhparam -out certs/dh 2048
	dependencies/openssl/apps/openssl req -x509 -newkey rsa:4096 -keyout certs/fullchain.pem -out certs/fullchain.pem -sha256 -days 3650 -nodes -subj "/C=XX/ST=it/L=Roma/O=Martello s.r.l/OU=Martello s.r.l/CN=martello.it"


clean_setup:
	cd dependencies && rm -rf openssl hostapd-eaphammer

libhostapd-eaphammer.so: setup

purge_output:
	@for file in output/*; do \
		echo "[] $$file"; \
		./purger.py $$file output_clean/$$(basename $$file)_gtc.csv output_clean/$$(basename $$file)_mschapv2.log; \
	done
	@find output -empty -delete
