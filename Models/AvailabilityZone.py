class AvailabilityZone:

    def __init__(self, zone: dict):
        self.name = zone['name']
        self.country = zone['country']
        self.default = bool(zone['isDefault'])
