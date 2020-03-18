from HttpLogic.RequestTypes import ApiRequests


class NameServers:
    """Nameservers model."""

    def __init__(self, connection: ApiRequests, nameservers: dict):
        self._connection = connection
        self.hostname = nameservers['hostname']
        self.ipv4 = nameservers['ipv4']
        self.ipv6 = nameservers['ipv6']
