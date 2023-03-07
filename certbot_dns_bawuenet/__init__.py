"""
The `~certbot_dns_bawuenet.dns_bawuenet` plugin automates the process of
completing a ``dns-01`` challenge (`~acme.challenges.DNS01`) by creating, and
subsequently removing, TXT records using the bawue.net MyBawue website.

Named Arguments
---------------
========================================  =====================================
``--dns-bawuenet:credentials``            Bawue.Net credentials_
                                          INI file. (Required)
========================================  =====================================


Credentials
-----------

.. code-block:: ini
   :name: credentials.ini
   :caption: Example credentials file:
   # MyBawue credentials used by Certbot
   dns_bawuenet_username = bawueuser
   dns_bawuenet_password = geheim


The path to this file can be provided interactively or using the
``--dns-bawuenet-credentials`` command-line argument. Certbot records the path
to this file for use during renewal, but does not store the file's contents.
"""
