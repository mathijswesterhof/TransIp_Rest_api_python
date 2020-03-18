from __future__ import annotations

from HttpLogic.RequestTypes import ApiRequests


class Contacts:
    """Contact collection object."""

    def __init__(self, connection: ApiRequests, contacts: list, domain):
        """Contact collection init"""
        self._connection = connection
        self.domain = domain
        self.contacts = [Contact(contact) for contact in contacts]

    def _serialize(self) -> list:
        """Return self as list of dicts."""
        return [c.serialize() for c in self.contacts]

    def update_contact(self):
        """Update contact info for domain."""
        # request = f'/domains/{self.domain}/contacts'
        raise NotImplementedError('put requests are for the next version, this is a placeholder')

    @staticmethod
    def build_self(connection: ApiRequests, domain: str) -> Contacts:
        request = f'/domains/{domain}/contacts'
        return connection.perform_get_request(
            request,
            lambda data: Contacts(connection, data['contacts'], domain)
        )


class Contact:
    """Contact object."""

    def __init__(self, contact: dict):
        """Contact init."""
        self.type = contact['type']
        self.first_name = contact['firstName']
        self.last_name = contact['lastName']
        self.company_name = contact['companyName']
        self.company_kvk = contact['companyKvk']
        self.company_type = contact['companyType']
        self.street = contact['street']
        self.number = contact['number']
        self.postal_code = contact['postalCode']
        self.city = contact['city']
        self.phone_number = contact['phoneNumber']
        self.fax_number = contact['faxNumber']
        self.email = contact['email']
        self.country = contact['country']

    def serialize(self) -> dict:
        """Return self as dict."""
        return {
            'type': self.type,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'companyName': self.company_name,
            'companyKvk': self.company_kvk,
            'companyType': self.company_type,
            'street': self.street,
            'number': self.number,
            'postalCode': self.postal_code,
            'city': self.city,
            'phoneNumber': self.phone_number,
            'faxNumber': self.fax_number,
            'email': self.email,
            'country': self.country
        }
