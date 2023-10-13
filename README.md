# certbot-dns-bawuenet
Certbot Plugin to handle DNS-01 challenges for bawue.net managed domains

Installation
------------

    pip install 'git+https://github.com/bawuenet/certbot-dns-bawuenet'

In case `certbot plugins` does not show the installed plugin, verify using `pip show certbot-dns-bawuenet` where it was installed.

If it has been installed to `/usr/local/lib/python*/site-packages` certbot _might_ not find it. Either symlink to
`/usr/lib/python*/site-packages` or reinstall using the `--prefix` parameter:

    pip install --prefix=/usr 'git+https://github.com/bawuenet/certbot-dns-bawuenet'

Named Arguments
---------------

To start using DNS authentication for bawuenet, pass the following arguments on certbot's command line:

Option|Description|
---|---|
`--authenticator dns-bawuenet`|select the authenticator plugin (Required)|
`--dns-bawuenet-credentials FILE`|bawue.net credentials INI file. (Required)|
`--dns-bawuenet-propagation-seconds NUM`|waiting time for DNS to propagate before asking the ACME server to verify the DNS record. (Default: 5, Recommended: \>= 600)|
`--dns-bawuenet-wait`|wait until the change is actually	present	in DNS which has the benefit of not having to set a large propagation delay.

Credentials
-----------

Credentials are stored in an .ini file and referenced using the `--dns-bawuenet-credentials` parameter.

    # MyBawue credentials used by Certbot
    dns_bawuenet_username = bawueuser
    dns_bawuenet_password = geheim

Usage
-----

    certbot -v \
        certonly \
        --authenticator dns-bawuenet \
        --dns-bawuenet-credentials /root/bwn.ini \
        --dns-bawuenet-wait \
        -d 'test.example.net'
