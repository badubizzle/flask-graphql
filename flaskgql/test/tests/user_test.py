
from hypothesis import given
import hypothesis.strategies as st
from urllib.parse import quote

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

@given(username=st.text(min_size=3)
#.filter(lambda s: len([c for c in s if not c.isalnum()]) == 0) 
.map(lambda s: s.strip()))
def test_create_user_with_user_name(username, client, gql, snapshot):        
    mutation = CREATE_USER_MUTATION
    variables = {'username': username}
    response = gql.mutate(mutation, variables)     
    print("USER===>>", response.json)
    assert response.status_code == 200, (mutation, response.data)
     
