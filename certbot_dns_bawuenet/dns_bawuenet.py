"""DNS Authenticator for bawue.net."""
import logging

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

from bawuenet.domains import DomainsAPI

logger = logging.getLogger(__name__)


class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for bawue.net
    This Authenticator uses the MyBawue interface to fulfill a dns-01 challenge.
    """

    description = "Obtain certificates using a DNS TXT record (if you are using bawue.net for DNS)."
    ttl = 60

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(
            add, default_propagation_seconds=5
        )
        add("credentials", help="bawue.net credentials INI file.")
        add("wait", help="Wait for DNS change to happen.", action="store_true")

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return (
            "This plugin configures a DNS TXT record to respond to a dns-01 challenge using "
            + "the MyBawue interface."
        )

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            "credentials",
            "bawue.net credentials INI file",
            {
                "username": "Username for MyBawue.",
                "password": "Password for MyBawue.",
            },
        )

    def _perform(self, domain, validation_name, validation):
        self._get_bawuenet_client().add_txt_record(
            domain, validation_name, validation, self.ttl
        )

    def _cleanup(self, domain, validation_name, validation):
        self._get_bawuenet_client().del_txt_record(
            domain, validation_name, validation, self.ttl
        )

    def _get_bawuenet_client(self):
        return _BawueNetClient(
            self.credentials.conf("username"),
            self.credentials.conf("password"),
            self.conf("wait"),
        )


class _BawueNetClient(object):
    """
    Wraps bawuenet/domainctl to be usable for certbot.
    """

    def __init__(self, username, password, wait):
        logger.debug("creating bawuenetclient")

        self.domainctl = DomainsAPI(username, password)
        self.wait = wait
        self.domains = self.domainctl.get_domains()
        logger.debug("Account owned domains: %s", ", ".join(self.domains))

    def find_customer_domain(self, fqdn):
        """
        Split a fqdn domain record into a host part and a domain part
        :param str fqdn: The fqdn record
        :returns (host, domain)
        :raises certbot.errors.PluginError: if an error occurs communicating with the MyBawue site
        """
        for domain in dns_common.base_domain_name_guesses(fqdn):
            if domain in self.domains:
                host = fqdn[: -(len(domain) + 1)]
                logger.debug(
                    "Matched fqdn %s to host %s in owned domain %s", fqdn, host, domain
                )
                return (host, domain)
        raise errors.PluginError(f"Domain {domain} not known")

    def add_txt_record(self, domain, record_name, record_content, record_ttl):
        """
        Add a TXT record using the supplied information.
        :param str domain: The domain to use to look up the managed zone.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :param int record_ttl: The record TTL (number of seconds that the record may be cached).
        :raises certbot.errors.PluginError: if an error occurs communicating with the MyBawue site
        """
        host, db_domain = self.find_customer_domain(domain)
        record_name = record_name[: -(len(db_domain) + 1)]
        self.domainctl.add_record(db_domain, record_name, "TXT", record_content)
        if self.wait:
            self.wait_for_add_record(db_domain, record_name, "TXT", record_content)

    def del_txt_record(self, domain, record_name, record_content, record_ttl):
        """
        Delete a TXT record using the supplied information.
        :param str domain: The domain to use to look up the managed zone.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :param int record_ttl: The record TTL (number of seconds that the record may be cached).
        :raises certbot.errors.PluginError: if an error occurs communicating with the MyBawue site
        """
        host, db_domain = self.find_customer_domain(domain)
        record_name = record_name[: -(len(db_domain) + 1)]
        self.domainctl.remove_record(db_domain, record_name, "TXT", record_content)
        if self.wait:
            self.wait_for_remove_record(db_domain, record_name, "TXT", record_content)

    def wait_for_add_record(self, domain, record_name, type, record_content):
        """
        Wait for a record to appear in the DNS
        """
        self.domainctl.wait_for_add_record(domain, record_name, type, record_content)

    def wait_for_remove_record(self, domain, record_name, type, record_content):
        """
        Wait for a record to be deleted in the DNS
        """
        # We're bailing early, no sense waiting here.
        return
        self.domainctl.wait_for_remove_record(domain, record_name, type, record_content)
