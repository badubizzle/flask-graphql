from hypothesis import given
import hypothesis.strategies as st

seen = set()

@st.composite
def deposit_withdrawal_pair(draw):
  deposit_amount=draw(st.integers(min_value=1, max_value=999999))
  withdrawal_amount=draw(st.integers(min_value=1, max_value = deposit_amount))
  

  return deposit_amount, withdrawal_amount

@given(username=st.text(min_size=5).map(lambda s: s.strip()), amounts = deposit_withdrawal_pair())
def test_withdraw_money(username, queries, amounts, client, gql, snapshot):
    
    global seen
    if username in seen:
      return
    
    seen.add(username)

    deposit_amount, withdrawal_amount = amounts
    response = gql.mutate(queries.CREATE_USER_MUTATION, {'username': username})
    assert response.status_code == 200
    user = response.json['data']['createUser']
    token = user['accessToken']
    # username = user['user']['username']
    assert username == user['user']['username']

    response = gql.mutate(queries.CREATE_ACCOUNT_MUTATION, {'username': username, 'token': token})
    assert response.status_code == 200
    account = response.json['data']['createAccount']['account']
    print(account)
    assert 'uuid' in account
    assert 'balance' in account
    assert account['balance'] == 0



    account_id = account['uuid']
    print("DEPOSIT===>", queries.DEPOSIT_MUTATION)
    print(account_id)
    response = gql.mutate(queries.DEPOSIT_MUTATION, {'accountUuid': account_id, 'token': token,'amount': deposit_amount})

    assert response.status_code == 200
    print(response.json)
    updated_account = response.json['data']['depositMoney']['account']
    assert 'uuid' in updated_account
    assert updated_account['uuid'] == account['uuid']
    assert 'balance' in updated_account
    assert updated_account['balance'] == deposit_amount


    response = gql.mutate(queries.WITHDRAW_MUTATION, {'accountUuid': account_id, 'token': token,'amount': withdrawal_amount})

    assert response.status_code == 200
    updated_account = response.json['data']['withdrawMoney']['account']
    assert 'uuid' in updated_account
    assert updated_account['uuid'] == account['uuid']
    assert 'balance' in updated_account
    assert updated_account['balance'] == deposit_amount - withdrawal_amount

