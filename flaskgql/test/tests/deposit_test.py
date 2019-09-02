
from hypothesis import given
import hypothesis.strategies as st

seen = set()

@given(username=st.text(min_size=5).map(lambda s: s.strip()),
amount=st.integers(min_value=1, max_value=999999))
def test_deposit_money(username,queries, amount, client, gql, snapshot):    
    
    global seen
    if username in seen:
      return
    
    seen.add(username)

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
    data = {'accountUuid': account_id, 'token': token,'amount': amount}
    print("DEPOSIT===>", queries.DEPOSIT_MUTATION, data)
    print(account_id)
    response = gql.mutate(queries.DEPOSIT_MUTATION, data)

    assert response.status_code == 200
    print("DEPOSIT RESPONSE===>>>", response.json)

    updated_account = response.json['data']['depositMoney']['account']
    assert 'uuid' in updated_account
    assert updated_account['uuid'] == account['uuid']
    assert 'balance' in updated_account
    assert updated_account['balance'] == amount

    # snapshot.assert_match(response.json)
