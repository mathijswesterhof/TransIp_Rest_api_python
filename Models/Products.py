from HttpLogic.RequestTypes import ApiRequests


class Products:

    def __init__(self, connection: ApiRequests, product: dict):
        self._connection = connection
        self.type = product['type']
        self.name = product['name']
        self.description = product['description']
        self.price = product['price']
        self.recurring_price = product['recurringPrice']
        self.specifications = None

    def get_elements(self):
        if self.specifications is None:
            request = f'/products/{self.name}/elements'
            self.specifications = self._connection.perform_get_request(
                request,
                lambda data: {item['name']: item for item in data['productElements']}
            )

        return self.specifications
