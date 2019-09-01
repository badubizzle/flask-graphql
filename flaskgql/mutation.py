import graphene
from .models import db

from .models import User, BankAccount
from .model_types import UserObject, AccountObject, ProtectedAccount, ProtectedUser
import uuid
from graphql import GraphQLError
from flask_graphql_auth import (
get_jwt_identity,
create_access_token,
create_refresh_token,
mutation_jwt_refresh_token_required,
mutation_jwt_required,
)
from .utils import match_account_user, match_current_user

class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
    
    user = graphene.Field(lambda: UserObject)
    access_token = graphene.String()
    refresh_token = graphene.String()

    def mutate(self, infor, username):
        user_uuid = str(uuid.uuid4())
        user = User(username=username, uuid=user_uuid)
        user_exists = User.query.filter_by(username=username).first()

        if not user_exists:
            db.session.add(user)
            db.session.commit()
            user_claims={'name': username, 'id': user_uuid}
            return CreateUser(user=user,access_token=create_access_token(user.username, user_claims=user_claims),
        refresh_token=create_refresh_token(user.username, user_claims=user_claims),)
        else:
            
            raise GraphQLError('Username already exists')
            # return "Error username already exists"


class CreateAccount(graphene.Mutation):
    class Arguments:
        token = graphene.String()        
        username = graphene.String(required=True)

    account = graphene.Field(ProtectedAccount)

    @mutation_jwt_required
    @match_current_user
    def mutate(self, info, username):                         
        user = User.query.filter_by(username=username).first()                
        if user is not None:            
            account_number = str(uuid.uuid4())
            account = BankAccount(uuid=account_number, balance=0)
            account.owner = user
            db.session.add(account)
            db.session.commit()
            return CreateAccount(account=account)
        else:
            raise GraphQLError('Unauthorized access')


class DepositMoney(graphene.Mutation):
    class Arguments:
        token = graphene.String()
        account_uuid = graphene.String(required=True)
        amount = graphene.Int(required=True)

    account = graphene.Field(ProtectedAccount)

    @mutation_jwt_required
    @match_account_user
    def mutate(self, info, account_uuid, amount, account=None):

        account = account or  BankAccount.query.filter_by(uuid=account_uuid).first()
        if not account:            
            raise GraphQLError('Could not deposit.')            
        if amount <= 0:
            raise GraphQLError('Could not deposit.')            

        account.balance = account.balance + amount
        db.session.add(account)
        db.session.commit()
        return DepositMoney(account=account)

class WithDrawMoney(graphene.Mutation):
    class Arguments:
        token = graphene.String()
        account_uuid = graphene.String(required=True)
        amount = graphene.Int(required=True)
    
    account = graphene.Field(ProtectedAccount)
    @mutation_jwt_required
    @match_account_user
    def mutate(self, info, account_uuid, amount, account=None):
        account = account or BankAccount.query.filter_by(uuid=account_uuid).first()
        if not account:
            raise GraphQLError('Could not withdraw.')            
        if amount <= 0:
            raise GraphQLError('Could not withdraw.')            
        if account.balance < amount:
            raise GraphQLError('Insufficient funds')            

        account.balance = account.balance - amount
        db.session.add(account)
        db.session.commit()
        return WithDrawMoney(account=account)
    

class AuthMutation(graphene.Mutation):
    class Arguments(object):
        username = graphene.String()
        password = graphene.String()

    access_token = graphene.String()
    refresh_token = graphene.String()
    @classmethod
    def mutate(cls, _, info, username, password):
        user_claims={'name': username}
        return AuthMutation(
        access_token=create_access_token(username, user_claims=user_claims),
        refresh_token=create_refresh_token(username, user_claims=user_claims),
        )
    

class RefreshMutation(graphene.Mutation):
    class Arguments(object):
        refresh_token = graphene.String()

    new_token = graphene.String()

    @classmethod
    @mutation_jwt_refresh_token_required
    def mutate(self, _):
        current_user = get_jwt_identity()
        return RefreshMutation(new_token=create_access_token(identity=current_user))


class Mutation(graphene.ObjectType):
    create_account = CreateAccount.Field()
    create_user = CreateUser.Field()
    deposit_money = DepositMoney.Field()
    withdraw_money = WithDrawMoney.Field()
    auth = AuthMutation.Field()
    refresh = RefreshMutation.Field()
