
from hypothesis import given
import hypothesis.strategies as st
from urllib.parse import quote

seen = set()

@given(username=st.text(min_size=3))
def test_create_accounts(username, queries, client, gql, snapshot):    
    global seen
    if username in seen:
      return
    
    seen.add(username)

    response = gql.mutate(queries.CREATE_USER_MUTATION, {'username': username})
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

    response = gql.mutate(queries.CREATE_ACCOUNT_MUTATION, {'username': username,'token': token})
    assert response.status_code == 200

    # snapshot.assert_match(response.json)
