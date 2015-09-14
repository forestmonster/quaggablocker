# UCSC AutoRTBH
Features
-----------------
* Talks to Quagga's Zebra daemon (extends JustinAzoff's bhr-client)
* Implements blocks manually, or in response to alerts from other sources, such as Bro

Kicking the tires
-----------------

    $ export BHR_HOST=https://127.0.0.1:8000
    $ export BHR_TOKEN=db4de92f933092b1f1f6665a742b7192a5eced77
    $ export BHR_IDENT=quagga
    $ python ./run.py

Install on FreeBSD
--------------------
* Copy quaggablocker.sh to /usr/local/etc/quaggablocker
* Copy quaggablocker.py to /usr/local/sbin/quaggablocker.py
* Copy bhr\_client directory to /usr/local/lib/python2.7/site-packages/
* Set chmod 555 /usr/local/etc/quaggablocker
* Set quaggablocker\_enable to YES in /etc/rc.conf
* Correct BHR\_TOKEN in /usr/local/etc/quaggablocker
* '''sudo service quaggablocker start'''

References
----------
* https://github.com/JustinAzoff/bhr-site
* https://github.com/JustinAzoff/bhr-client
* https://github.com/JustinAzoff/bhr-bro
