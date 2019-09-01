from .model_types import UserObject, AccountObject, ProtectedAccount, ProtectedUser
from .models import User, BankAccount

import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphql import GraphQLError
from flask_graphql_auth import (
get_jwt_identity,
query_jwt_required,
)
from .utils import match_account_user

class UsersField(SQLAlchemyConnectionField):
    pass


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    user = graphene.Field(
    type=ProtectedUser,
    token=graphene.String(),
    uuid=graphene.Argument(type=graphene.String, required=False),
    username=graphene.Argument(type=graphene.String, required=False),)
    account = graphene.Field(
        type=ProtectedAccount,
        token=graphene.Argument(type=graphene.String, required=True),
        account_uuid=graphene.Argument(type=graphene.String, required=True),
    )

   
    @staticmethod
    @query_jwt_required
    @match_account_user
    def resolve_account(args,info, account_uuid, account=None):                        
        
        account = account or BankAccount.query.filter_by(uuid=account_uuid).first()

        if not account:
            raise GraphQLError("Invalid account")
        
        return account        


    
    @staticmethod
    @query_jwt_required
    def resolve_user(args,info, uuid=None, username = None):                        
        query = UserObject.get_query(info=info)
        if not uuid and not username:
            raise GraphQLError("Username or uuid required.")

        if uuid:
            query = query.filter(User.uuid == id)
        elif username:
            query = query.filter(User.username == username)
        
        user = query.first()
        current_user = get_jwt_identity()
        if current_user != user.username:
            raise GraphQLError("Unauthorized access or invalid token.")
        
        return  user #UserObject(username=user.username)



