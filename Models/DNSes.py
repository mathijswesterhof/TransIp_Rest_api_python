from __future__ import annotations

from HttpLogic.RequestTypes import ApiRequests


class DNSes:
    """Collection of DNS."""

    def __init__(self, connection: ApiRequests, dnses: list, domain):
        """Collection of DNS init."""
        self._connection = connection
        self.domain = domain
        self.dnses = [DNS(connection, d) for d in dnses]

    def _serialize(self) -> list:
        """Return self as list of dict."""
        return [d.serialize() for d in self.dnses]

    def add_dns(self, dns: dict) -> bool:
        """Add dns to list of DNSes."""
        request = f"/domains/{self.domain}/dns"
        response = self._connection.perform_post_request(
            request,
            dns
        )

        if response:
            self.dnses.append(DNS(self._connection, dns))

        return response

    def update_dnses(self):
        """Update all DNSes."""
        # request = f"/domains/{self.domain}/dns"
        # data = self._serialize()
        raise NotImplementedError('put not implemented')

    @staticmethod
    def build_self(connection: ApiRequests, domain: str) -> DNSes:
        request = f'/domains/{domain}/dns'
        return connection.perform_get_request(
            request,
            lambda data: DNSes(connection, data['dnsEntries'], domain)
        )


class DNS:
    """DNS model."""
    def __init__(self, connection: ApiRequests, dns: dict):
        """DNS init."""
        self._connection = connection
        self.name = dns['name']
        self.expire = dns['expire']
        self.type = dns['type']
        self.content = dns['content']

    def serialize(self) -> dict:
        """Return self as dict."""
        return {
            'name': self.name,
            'expire': self.expire,
            'type': self.type,
            'content': self.content
        }

    def update(self):
        """Update self."""
        raise NotImplementedError('patch requests are for the next version, this is a placeholder')

    def delete(self):
        """delete self."""
        raise NotImplementedError('Delete request not implemented')
