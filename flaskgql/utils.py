from functools import wraps
from .models import BankAccount
from flask_graphql_auth import get_jwt_identity
from graphql import GraphQLError

def match_current_user(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        current_user = get_jwt_identity()
        if kwargs['username'] != current_user:
            raise GraphQLError("Unauthorized access or nvalid token")        
        return f(*args, **kwargs)
   
    return wrap

def match_account_user(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        print(kwargs)
        current_user = get_jwt_identity()
        account_uuid = kwargs['account_uuid']
        account = BankAccount.query.filter_by(uuid=account_uuid).first()

        if not account:            
            raise GraphQLError("Unauthorized access or nvalid token or invalid account id3")        
        if account.owner.username != current_user:
            raise GraphQLError("Unauthorized access or nvalid token or invalid account id")        

        kwargs['account'] = account    
        return f(*args, **kwargs)
   
    return wrap