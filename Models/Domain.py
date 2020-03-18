from __future__ import annotations
from datetime import datetime

from HttpLogic.RequestTypes import ApiRequests
from Models import Branding, Contacts, DNSes, NameServers


class Domain:
    """Domain object."""

    def __init__(self, connection: ApiRequests, domain: dict):
        """Domain init."""
        self._connection = connection
        self.name = domain['name']
        self.auth_code = domain['authCode']\
            if 'authCode' in domain else None
        self.is_transfer_locked = bool(domain['isTransferLocked'])\
            if 'isTransferLocked' in domain else None
        self.registration_date = datetime.strptime(domain['registrationDate'], '%Y-%m-%d').date()\
            if 'registrationDate' in domain else None
        self.renewal_date = datetime.strptime(domain['renewalDate'], '%Y-%m-%d').date()\
            if 'renewalDate' in domain else None
        self.is_whitelabel = bool(domain['isWhitelabel'])\
            if 'isWhitelabel' in domain else None
        self.cancellation_date = datetime.strptime(domain['cancellationDate'], '%Y-%m-%d %H:%M:%S')\
            if 'cancellationDate' in domain else None
        self.cancellation_status = domain['cancellationStatus']\
            if 'cancellationStatus' in domain else None
        self.is_dns_only = bool(domain['isDnsOnly'])\
            if 'isDnsOnly' in domain else None
        self.tags = domain['tags']\
            if 'tags' in domain else None
        self.branding = domain['branding']\
            if 'tags' in domain else None
        self.contacts = domain['contacts']\
            if 'tags' in domain else None
        self.dnses = domain['dnses']\
            if 'tags' in domain else None
        self.name_servers = domain['nameservers']\
            if 'tags' in domain else None

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

    def add_dns_entry(
        self,
        name: str,
        expire: int,
        type: str,
        content: str
    ):
        if self.dnses is None:
            self.dnses = DNSes(self._connection, [], self.name)

        self.dnses.add_dns({
            'name': name,
            'expire': expire,
            'type': type.upper(),
            'content': content
        })

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
        if self.branding is None:
            self.branding = Branding.build_self(self._connection, self.name)

        return self.branding

    def get_contacts(self) -> Contacts:
        """Get contacts for domain."""
        if self.contacts is None:
            self.contacts = Contacts.build_self(self._connection, self.name)

        return self.contacts

    def get_dnses(self) -> DNSes:
        """Get dns list for domain."""
        if self.dnses is None:
            self.dnses = DNSes.build_self(self._connection, self.name)

        return self.dnses

    def update_domain(self):
        """Update domain info."""
        raise NotImplementedError('put requests are for the next version, this is a placeholder')

    def delete_domain(self):
        """Send termination request for domain."""
        raise NotImplementedError('delete requests are for the next version, this is a placeholder')
