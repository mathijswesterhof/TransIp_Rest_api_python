class AvailabilityZone:
    """AvailabilityZone Model."""

    def __init__(self, zone: dict):
        """AvailabilityZone init."""
        self.name = zone['name']
        self.country = zone['country']
        self.default = bool(zone['isDefault'])
