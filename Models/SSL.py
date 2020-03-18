from datetime import datetime

from HttpLogic.RequestTypes import ApiRequests


class SSL:
    """SSL model."""

    def __init__(self, connection: ApiRequests, ssl: dict):
        """SSL init."""
        self._connection = connection
        self.certificate_id = ssl['certificateId']
        self.common_name = ssl['commonName']
        self.expiration_date = datetime.strptime(ssl['expirationDate'], '%Y-%m-%d').date()
        self.status = ssl['status']
