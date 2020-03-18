from datetime import datetime

from HttpLogic.RequestTypes import ApiRequests


class Invoice:
    """Invoice model."""
    def __init__(self, connection: ApiRequests, invoice: dict):
        """Invoice init."""
        self._connection = connection
        self.invoice_number = invoice['invoiceNumber']
        self.creation_date = datetime.strptime(invoice['creationDate'], '%Y-%m-%d').date()
        self.pay_date = datetime.strptime(invoice['payDate'], '%Y-%m-%d').date()
        self.due_date = datetime.strptime(invoice['dueDate'], '%Y-%m-%d').date()
        self.invoice_status = invoice['invoiceStatus']
        self.currency = invoice['currency']
        self.total_amount = invoice['totalAmount']
        self.total_amount_incl_vat = invoice['totalAmountInclVat']
        self.invoice_items = None

    def get_items(self) -> dict:
        """Request aditional info for invoice."""
        if self.invoice_items is not None:
            return self.invoice_items

        request = f'/invoices/{self.invoice_number}/invoice-items'
        self.invoice_items = self._connection.perform_get_request(
            request,
            lambda data: data['invoiceItems']
        )
        return self.invoice_items
