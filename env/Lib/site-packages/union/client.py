import json
import requests
import union
from six import text_type


#
# Union Errors
#

class UnionError(Exception):
    pass

class APIError(UnionError):
    pass

class AuthenticationError(UnionError):
    pass

class ValidationError(UnionError):
    pass


#
# Union API Client
#

class UnionClient(object):
    def __init__(self, **kwargs):
        self.content_type =  'application/json'
        self.api_key =       union.api_key
        self.host =          union.host
        self.api_version =   union.api_version
        self.api_namespace = union.api_namespace
        self.protocol =      union.protocol
        self.subpath =       kwargs.get('subpath', '')

    def _headers(self, action=None):
        default = {'Accept': 'application/json',
                   'Authorization': 'Token %s' % (self.api_key,)}

        if action and action.lower() is not 'get':
            return dict(default, **{'Content-Type': 'application/json'})
        return default

    def _model_path_name(self, model):
        if isinstance(model, type):
            class_name = self._look_up_plural_from_model(model)
        else:
            class_name = self._look_up_plural_from_model(model.__class__)
        return '/%s' % class_name

    def _create_url(self, model, **params):
        url = "%s://%s%s" % (self.protocol, self.host, self._model_path_name(model))
        url += self.subpath
        if params:
            if 'id' in list(params):
                id_param = params.pop('id')
                url += '/%s' % id_param
            for k, v in list(params.items()):
                url += '&%s=%s' % (k, v)
        return url

    def _is_valid(self, response):
        return True if (200 <= response.status_code < 300) else False

    def _look_up_plural_from_model(self, model):
        results = [x for x in union.MODEL_MAP if x['model'] == model]
        if results:
            return results[0]['plural']

    def _look_up_model_name(self, name_type, name):
        results = [x for x in union.MODEL_MAP if x[name_type] == name.lower()]
        if results:
            return results[0]['model']

    def _get_model_from_name(self, name):
        if not isinstance(name, text_type):
            return name

        model = self._look_up_model_name('name', name)
        return model or self._look_up_model_name('plural', name)

    def _parse_response(self, response):
        if response.content:
            return self._from_json(json.loads(response.content))

    def _from_json(self, json_data):
        for k, v in list(json_data.items()):
            model = self._get_model_from_name(k)

            if isinstance(v, list):
                return [self._from_json({model: obj}) for obj in v]
            elif isinstance(v, dict) and not isinstance(v, union.BaseModel):
                return model(**v)
            return json_data

    def make_request(self, model, action, url_params={}, post_data=None):
        '''
        Send request to API then validate, parse, and return the response
        '''
        url = self._create_url(model, **url_params)
        headers = self._headers(action)

        try:
            response = requests.request(action, url, headers=headers, data=post_data)
        except Exception as e:
            raise APIError("There was an error communicating with Union: %s" % e)

        if not self._is_valid(response):
            raise ValidationError("The Union response returned an error: %s" % response.content)

        return self._parse_response(response)