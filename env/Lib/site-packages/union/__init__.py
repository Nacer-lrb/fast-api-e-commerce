api_key = ''
api_namespace = 'api'
api_version = "v1"
host = "api.unionbilling.com"
protocol = "https"

# Union Models
from union.models import (
    BaseModel,
    Customer,
    Invoice,
    Vendor,
    Bill,
    Order,
    Item,
    Organization,
    PaymentMethod,
    Payments,
    PurchaseOrder,
    Tax
)

# API Client
from union.client import UnionClient

# Union models
MODEL_MAP = [
        {'model': Customer, 'name': 'customer', 'plural': 'customers'},
        {'model': Invoice, 'name': 'invoice', 'plural': 'invoices'},
        {'model': Vendor, 'name': 'vendor', 'plural': 'vendors'},
        {'model': Bill, 'name': 'bill', 'plural': 'bills'},
        {'model': Order, 'name': 'order', 'plural': 'orders'},
        {'model': Item, 'name': 'item', 'plural': 'items'},
        {'model': Organization, 'name': 'organization', 'plural': 'organizations'},
        {'model': PaymentMethod, 'name': 'payment_method', 'plural': 'payment_methods'},
        {'model': Payments, 'name': 'payments', 'plural': 'payments'},
        {'model': PurchaseOrder, 'name': 'purchase_order', 'plural': 'purchase_orders'},
        {'model': Tax, 'name': 'tax', 'plural': 'taxes'},
]
