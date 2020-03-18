from HttpLogic.Authenticate import TransIpAuthenticate
from HttpLogic.RequestTypes import ApiRequests
from HttpLogic.Exceptions import NotFoundError

from Models import *


class TransIpRestfulAPI:

    endpoint = 'api.transip.nl'
    version = 'v6'

    def __init__(self, login: str, key_url: str):
        """Set Api with credentials."""
        self.auth = TransIpAuthenticate(login, key_url, self.get_endpoint())
        self.requests = ApiRequests(self.auth, self.get_endpoint())

    # ### Get requests ### #

    def get_availability_zones(self) -> AvailabilityZone:
        return self.requests.perform_get_request(
            '/availability-zones',
            lambda data: [AvailabilityZone(zone) for zone in data['availability-zones']]
        )

    def get_branding_for_domain(self, domain: str) -> Branding:
        return Branding.build_self(self.requests, domain)

    def get_contacts_for_domain(self, domain: str) -> Contacts:
        return Contacts.build_self(self.requests, domain)

    def get_dns_for_domain(self, domain: str) -> DNSes:
        return DNSes.build_self(self.requests, domain)

    def get_domains(self, tags: list = None) -> list:
        tag = '' if tags is None or len(tags) == 0 else '?tags=' ','.join(tags)

        request = f'/domains{tag}'
        response = self.requests.perform_get_request(
            request,
            lambda data: [Domain(self.requests, domain) for domain in data['domains']]
        )

        return response

    def get_domain(self, domain_name: str) -> Domain:
        request = f'/domains/{domain_name}'
        return self.requests.perform_get_request(
            request,
            lambda data: Domain(self.requests, data['domain'])
        )

    def get_endpoint(self) -> str:
        return f'https://{self.endpoint}/{self.version}'

    def get_invoice(self, invoice_number: str) -> Invoice:
        request = f'/invoices/{invoice_number}'
        return self.requests.perform_get_request(
            request,
            lambda data: Invoice(self.requests, data['invoice'])
        )

    def get_invoices(self) -> [Invoice]:
        return self.requests.perform_get_request(
            '/invoices',
            lambda data: [Invoice(self.requests, i) for i in data['invoices']]
        )

    def get_invoice_as_pdf(self, invoice_number: str) -> str:
        request = f'/invoices/{invoice_number}/pdf'
        return self.requests.perform_get_request(
            request,
            lambda data: data['pdf']
        )

    def get_products(self) -> [Products]:
        return self.requests.perform_get_request(
            '/products',
            lambda data: [
                Products(self.requests, {**item, 'type': product_type}) for product_type, items
                in data['products'].items() for item in items
            ]
        )

    def test_connection(self) -> bool:
        return self.requests.perform_get_request(
            '/api-test',
            lambda data: bool(data['ping'] == 'pong')
        )

    # ### Post requests ### #

    def create_domain(
            self,
            domain_name: str,
            contacts: [Contacts] = None,
            name_servers: [NameServers] = None,
            dnses: DNSes = None,
            update_model: bool = True
    ):
        self.transfer_domain(
            domain_name,
            '',
            contacts,
            name_servers,
            dnses,
            update_model
        )

    def create_dns_entry_for_domain(
            self,
            domain: str,
            name: str,
            expire: int,
            dtype: str,
            content: str
    ):
        domain = Domain(self.requests, {'name': domain})
        domain.add_dns_entry(name, expire, dtype.upper(), content)

    def transfer_domain(
            self,
            domain_name: str,
            transfer_code: str,
            contacts: [Contacts] = None,
            name_servers: [NameServers] = None,
            dnses: DNSes = None,
            update_model: bool = True
    ):
        domain = {
            'name': domain_name,
            'contacts': [] if contacts is None else contacts,
            'nameservers': [] if name_servers is None else name_servers,
            'dnses': [] if dnses is None else dnses
        }

        if transfer_code is not None and transfer_code is not '':
            domain['authCode'] = transfer_code

        self.requests.perform_post_request(
            '/domains',
            domain
        )
        if update_model:
            try:
                return self.get_domain(domain_name)
            except NotFoundError:
                pass

        return Domain(self.requests, {'name': domain_name})