from .models import User, BankAccount
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from flask_graphql_auth import AuthInfoField

class AccountObject(SQLAlchemyObjectType):
    class Meta:
        model = BankAccount
        interfaces = (graphene.relay.Node, )

class UserObject(SQLAlchemyObjectType):
   class Meta:
       model = User
       interfaces = (graphene.relay.Node, )
    
    
   @classmethod
   def process_args(cls, query, root, connection, args, **kwargs):
       print(query)
       return query

class ProtectedAccount(graphene.Union):
    class Meta:
        types = (AccountObject, AuthInfoField)

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, AccountObject) or isinstance(instance, BankAccount):
            return AccountObject
        
        return type(instance)

class ProtectedUser(graphene.Union):
    class Meta:
        types = (UserObject, AuthInfoField)
    
    

    @classmethod
    def resolve_type(cls, instance, info):
        print(instance, info, cls)
        if isinstance(instance,User) or isinstance(instance, UserObject):
            return UserObject        
        return type(instance)
