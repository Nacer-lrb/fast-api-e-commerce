import json
import union
from six import text_type

#
# Abstract Base Model
#

class BaseModel(object):
    def __init__(self, **attrs):
        for k, v in list(attrs.items()):
            self.__setattr__(k, v)

    def __repr__(self):
        return text_type('< union.%s(%s) >' % (type(self).__name__, self))

    def __str__(self):
        return self._to_json

    def __setattr__(self, k, v=None):
        super(BaseModel, self).__setattr__(k, v)

    @property
    def _to_dict(self):
        return dict((k, v) for k, v in list(self.__dict__.items()) if not k.startswith('_'))

    @property
    def _to_json(self):
        return json.dumps(self._to_dict, sort_keys=True, indent=4)

    @classmethod
    def _new_api_client(cls, **kwargs):
        return union.UnionClient(**kwargs)

    @classmethod
    def all(cls):
        '''
        Returns multiple Union objects
        '''
        client = cls._new_api_client()
        return client.make_request(cls, 'get')

    @classmethod
    def filter(cls, **items):
        '''
        Returns multiple Union objects with search params
        '''
        client = cls._new_api_client(subpath='/search')
        items_dict = dict((k, v) for k, v in list(items.items()))
        json_data = json.dumps(items_dict, sort_keys=True, indent=4)
        return client.make_request(cls, 'post', post_data=json_data)

    @classmethod
    def get(cls, id):
        '''
        Look up one Union object
        '''
        client = cls._new_api_client()
        return client.make_request(cls, 'get', url_params={'id': id})

    def save(self):
        '''
        Save an instance of a Union object
        '''
        client = self._new_api_client()
        params = {'id': self.id} if hasattr(self, 'id') else {}
        action =  'patch' if hasattr(self, 'id') else 'post'
        saved_model = client.make_request(self, action, url_params=params, post_data=self._to_json)
        self.__init__(**saved_model._to_dict)

    @classmethod
    def delete(cls, id):
        '''
        Destroy a Union object
        '''
        client = cls._new_api_client()
        return client.make_request(cls, 'delete', url_params={'id': id})

#
# Union Objects
#

class Customer(BaseModel):
    pass

class Invoice(BaseModel):
    pass

class Vendor(BaseModel):
    pass

class Bill(BaseModel):
    pass

class Order(BaseModel):
    pass

class Item(BaseModel):
    pass

class Organization(BaseModel):
    pass

class PaymentMethod(BaseModel):
    pass

class Payments(BaseModel):
    pass

class PurchaseOrder(BaseModel):
    pass

class Tax(BaseModel):
    pass
