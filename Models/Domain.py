from __future__ import annotations
from datetime import datetime

from HttpLogic.RequestTypes import ApiRequests
from Models import Branding, Contacts, DNSes


class Domain:
    """Domain object."""

    def __init__(self, connection: ApiRequests, domain: dict):
        """Domain init."""
        self._connection = connection
        self.name = domain['name']
        self.auth_code = domain['authCode']
        self.is_transfer_locked = bool(domain['isTransferLocked'])
        self.registration_date = datetime.strptime(domain['registrationDate'], '%Y-%m-%d').date()
        self.renewal_date = datetime.strptime(domain['renewalDate'], '%Y-%m-%d').date()
        self.is_whitelabel = bool(domain['isWhitelabel'])
        self.cancellation_date = datetime.strptime(domain['cancellationDate'], '%Y-%m-%d %H:%M:%S')
        self.cancellation_status = domain['cancellationStatus']
        self.is_dns_only = bool(domain['isDnsOnly'])
        self.tags = domain['tags']

    def _serialize(self) -> dict:
        """Return self as dict."""
        return {
            'name': self.name,
            'authCode': self.auth_code,
            'isTransferLocked': self.is_transfer_locked,
            'registrationDate': self.registration_date.strftime('%Y-%m-%d'),
            'renewalDate': self.renewal_date.strftime('%Y-%m-%d'),
            'isWhitelabel': self.is_whitelabel,
            'cancellationDate': self.cancellation_date.strftime('%Y-%m-%d %H:%M:%S'),
            'cancellationStatus': self.cancellation_status,
            'isDnsOnly': self.is_dns_only,
            'tags': self.tags
        }

    def update_transfer_locked(self, state: bool):
        """Update transfer state."""
        self.is_transfer_locked = state

    def update_white_label(self, state: bool):
        """Update whitelabel state."""
        self.is_whitelabel = state

    def update_tags(self, tags: list):
        """Update tags."""
        self.tags = tags

    def get_branding(self) -> Branding:
        """Get branding for domain."""
        return Branding.build_self(self._connection, self.name)

    def get_contacts(self) -> Contacts:
        """Get contacts for domain."""
        return Contacts.build_self(self._connection, self.name)

    def get_dnses(self) -> DNSes:
        """Get dns list for domain."""
        return DNSes.build_self(self._connection, self.name)

    def update_domain(self):
        """Update domain info."""
        raise NotImplementedError('put requests are for the next version, this is a placeholder')

    def delete_domain(self):
        """Send termination request for domain."""
        raise NotImplementedError('delete requests are for the next version, this is a placeholder')

    @staticmethod
    def create_domain(
            connection: ApiRequests,
            domain_name: str,
            contacts: list,
            name_servers: list,
            dns_entries: list,
    ) -> bool:
        return connection.perform_post_request(
            '/domains',
            {
                'domainName': domain_name,
                'contacts': contacts,
                'nameservers': name_servers,
                'dnsEntries': dns_entries
            }
        )

    @staticmethod
    def transfer_domain(
            connection: ApiRequests,
            domain_name: str,
            auth_code: str,
            contacts: list,
            name_servers: list,
            dns_entries: list,
    ) -> bool:
        return connection.perform_post_request(
            '/domains',
            {
                'domainName': domain_name,
                'authCode': auth_code,
                'contacts': contacts,
                'nameservers': name_servers,
                'dnsEntries': dns_entries
            }
        )
