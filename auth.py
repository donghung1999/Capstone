import json
import os
from flask import abort, request
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = [os.getenv('ALGORITHMS')]
API_AUDIENCE = os.getenv('API_AUDIENCE')

## AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
def get_token_auth_header():
    if not request.headers.get('Authorization', None): raise AuthError({
            'code': 'can_not_find_authorization_in_header',
            'description': 'Can not find Authorization in header 1'
        }, 401)
    getHeaderAuthorizationItem = request.headers.get('Authorization', None).split()
    if getHeaderAuthorizationItem[0].lower() != 'bearer': raise AuthError({
            'code': 'can_not_fund_bearer_in_header',
            'description': 'Can not find Bearer in header 2'
        }, 401)
    elif len(getHeaderAuthorizationItem) == 1: raise AuthError({
            'code': 'can_not_fund_token_in_header',
            'description': 'Can not find token in header 3'
        }, 401)
    elif len(getHeaderAuthorizationItem) > 2: raise AuthError({
            'code': 'header_format_not_match_bearer_format',
            'description': 'Header format not match bearer format 4'
        }, 401)
    return getHeaderAuthorizationItem[1]

def check_permissions(getInputPermission, getInputpayload):
    if 'permissions' not in getInputpayload:
        raise AuthError({
            'code': 'can_not_find_permission_in_header',
            'description': 'Can not find permission in header',
        }, 401)
    if getInputPermission not in getInputpayload['permissions']:
        raise AuthError({
            'code': 'can_not_find_permission',
            'description': 'Can not find permission'
        }, 403)
    return True

def verify_decode_jwt(input):
    getInputRsaKey = {}
    if 'kid' not in jwt.get_unverified_header(input):
        raise AuthError({
            'code': 'authorization_wrong_format',
            'description': 'Authorization wrong format'
        }, 401)

    for key in json.loads(urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json').read())['keys']:
        if key['kid'] == jwt.get_unverified_header(input)['kid']:
            getInputRsaKey = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if getInputRsaKey:
        try:
            return jwt.decode(
                input,
                getInputRsaKey,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
        except Exception as e:
            raise AuthError({
                'code': 'auth_error',
                'description': e
            }, 401)
    raise AuthError({
        'code': 'auth_error',
        'description': 'Can not find key in header'
    }, 401)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator