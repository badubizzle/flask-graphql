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
from hypothesis import given
import hypothesis.strategies as st
from urllib.parse import quote


seen = set()
@st.composite
def list_unique_string(draw):    
    data = st.text(min_size=5).filter()
    return data


@given(username=st.text(min_size=3))
def test_create_accounts(username, client, gql, snapshot):

    global seen

    if username in seen:
      return
    seen.add(username)

    response = gql.mutate(CREATE_USER_MUTATION, {'username': username})
    assert response.status_code == 200
    assert 'data' in response.json 

    print(response.json)
    assert 'createUser' in response.json['data']  
    user = response.json['data']['createUser']

    assert 'accessToken' in user
    token = user['accessToken']

    assert 'user' in user
    assert 'username' in user['user']

    username = user['user']['username']

    response = gql.mutate(CREATE_ACCOUNT_MUTATION, {'username': username,'token': token})
    assert response.status_code == 200

    # snapshot.assert_match(response.json)

@given(username=st.text(min_size=5).map(lambda s: s.strip()),
amount=st.integers(min_value=1, max_value=999999))
def test_deposit_money(username, amount, client, gql, snapshot):
    global seen

    if username in seen:
      return
    seen.add(username)
    response = gql.mutate(CREATE_USER_MUTATION, {'username': username})
    assert response.status_code == 200
    user = response.json['data']['createUser']
    token = user['accessToken']
    # username = user['user']['username']
    assert username == user['user']['username']

    response = gql.mutate(CREATE_ACCOUNT_MUTATION, {'username': username, 'token': token})
    assert response.status_code == 200
    account = response.json['data']['createAccount']['account']
    print(account)
    assert 'uuid' in account
    assert 'balance' in account
    assert account['balance'] == 0



    account_id = account['uuid']
    data = {'accountUuid': account_id, 'token': token,'amount': amount}
    print("DEPOSIT===>", DEPOSIT_MUTATION, data)
    print(account_id)
    response = gql.mutate(DEPOSIT_MUTATION, data)

    assert response.status_code == 200
    print("DEPOSIT RESPONSE===>>>", response.json)

    updated_account = response.json['data']['depositMoney']['account']
    assert 'uuid' in updated_account
    assert updated_account['uuid'] == account['uuid']
    assert 'balance' in updated_account
    assert updated_account['balance'] == amount

    # snapshot.assert_match(response.json)

@st.composite
def deposit_withdrawal_pair(draw):
  deposit_amount=draw(st.integers(min_value=1, max_value=999999))
  withdrawal_amount=draw(st.integers(min_value=1, max_value = deposit_amount))
  

  return deposit_amount, withdrawal_amount

@given(username=st.text(min_size=5).map(lambda s: s.strip()), amounts = deposit_withdrawal_pair())
def test_withdraw_money(username, amounts, client, gql, snapshot):

    global seen

    if username in seen:
      return
    seen.add(username)

    deposit_amount, withdrawal_amount = amounts
    response = gql.mutate(CREATE_USER_MUTATION, {'username': username})
    assert response.status_code == 200
    user = response.json['data']['createUser']
    token = user['accessToken']
    # username = user['user']['username']
    assert username == user['user']['username']

    response = gql.mutate(CREATE_ACCOUNT_MUTATION, {'username': username, 'token': token})
    assert response.status_code == 200
    account = response.json['data']['createAccount']['account']
    print(account)
    assert 'uuid' in account
    assert 'balance' in account
    assert account['balance'] == 0



    account_id = account['uuid']
    print("DEPOSIT===>", DEPOSIT_MUTATION)
    print(account_id)
    response = gql.mutate(DEPOSIT_MUTATION, {'accountUuid': account_id, 'token': token,'amount': deposit_amount})

    assert response.status_code == 200
    print(response.json)
    updated_account = response.json['data']['depositMoney']['account']
    assert 'uuid' in updated_account
    assert updated_account['uuid'] == account['uuid']
    assert 'balance' in updated_account
    assert updated_account['balance'] == deposit_amount


    response = gql.mutate(WITHDRAW_MUTATION, {'accountUuid': account_id, 'token': token,'amount': withdrawal_amount})

    assert response.status_code == 200
    updated_account = response.json['data']['withdrawMoney']['account']
    assert 'uuid' in updated_account
    assert updated_account['uuid'] == account['uuid']
    assert 'balance' in updated_account
    assert updated_account['balance'] == deposit_amount - withdrawal_amount

