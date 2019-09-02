import os
import pytest
from flaskgql.main import app as flask_app
from flaskgql.main import db

from flask_migrate import upgrade

@pytest.yield_fixture(scope='session')
def app():
    """
    Setup our flask test app, this only gets executed once.

    :return: Flask app
    """
    params = {
        'DEBUG': False,
        'TESTING': True,
    }
    _app = flask_app
    print(_app)
    _app.config['TESTING'] = True
    _app.config['DEBUG'] = False

    basedir = os.path.abspath(os.path.dirname(__file__))

    _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.sqlite')

    with _app.app_context():
        upgrade()

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app
    db.drop_all()
    db.engine.execute("DROP TABLE alembic_version")
    ctx.pop()
    



@pytest.yield_fixture(scope='function')
def client(app):
    """
    Setup an app client, this gets executed for each test function.

    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()

class QueryHelper(object):
    client = None
    def __init__(self, client=None):
        self.client = client

    def mutate(self,query, variables=None):
        if variables:
            # do post
            import json
            data = {'query': query, 'variables': json.dumps(variables)}
            url = "/graphql"
            response = self.client.post(url, data=data)
            return response
        else:
            url = '/graphql?query=mutation '+query
            response = self.client.post(url)
            return response

    def query(self,query):
        url = '/graphql?query=query '+query
        response = self.client.get(url)
        return response

class Queries(object):
    
    CREATE_ACCOUNT_MUTATION = """
          mutation createAccount($username: String!, $token: String!){
           createAccount(username: $username, token: $token){
              account{
              ... on AccountObject{
                uuid
                balance
              }
              ... on AuthInfoField{
                    message
              }
            }
          }
          }
     """
    DEPOSIT_MUTATION = """
     mutation depositMoney($accountUuid: String!, $amount: Int!, $token: String!){
       depositMoney(accountUuid: $accountUuid, amount: $amount, token: $token){
         account{
           ... on AccountObject{
             balance
             uuid
           }
           ... on AuthInfoField{
             message
           }
         }
       }
     }
     """

    WITHDRAW_MUTATION = """
    mutation withdrawMoney($accountUuid: String!, $amount: Int!, $token: String!){
      withdrawMoney(accountUuid: $accountUuid, amount: $amount, token: $token){
        account{
          ... on AccountObject{
            balance
            uuid
          }
          ... on AuthInfoField{
            message
          }
        }
      }
    }
    """

    CREATE_USER_MUTATION = """
     mutation createUser($username: String!) {
          createUser(username: $username){
          accessToken
          refreshToken
          user{
               username
          }
          }
     }
     """
@pytest.fixture(scope='function')
def gql(client):    
    query_helper = QueryHelper(client=client)
    
    return query_helper

@pytest.fixture(scope='function')
def queries():
    return Queries()
    
     


