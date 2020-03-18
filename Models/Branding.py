from __future__ import annotations

from HttpLogic.RequestTypes import ApiRequests


class Branding:

    def __init__(self, connection: ApiRequests, branding: dict):
        self._connection = connection
        self.domain = branding['domain']
        self.company_name = branding['companyName']
        self.support_email = branding['supportEmail']
        self.company_url = branding['companyUrl']
        self.terms_of_usage_url = branding['termsOfUsageUrl']
        self.banner_1 = branding['bannerLine1']
        self.banner_2 = branding['bannerLine2']
        self.banner_3 = branding['bannerLine3']

    def _serialize(self) -> dict:
        return {
            'companyName': self.company_name,
            'supportEmail': self.support_email,
            'companyUrl': self.company_url,
            'termsOfUsageUrl': self.terms_of_usage_url,
            'bannerLine1': self.banner_1,
            'bannerLine2': self.banner_2,
            'bannerLine3': self.banner_3
        }

    def update_branding(self):
        # request = f'/domains/{self.domain}/branding'
        raise NotImplementedError('put requests are for the next version, this is a placeholder')

    @staticmethod
    def build_self(connection: ApiRequests, domain: str) -> Branding:
        request = f'/domains/{domain}/branding'
        return connection.perform_get_request(
            request,
            lambda data: Branding(connection, {**data['branding'], 'domain': domain})
        )
