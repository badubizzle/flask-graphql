def test_create_user_with_user_name(client,gql, snapshot):

     mutation = """
     mutation{
  createUser(username: "Kofi"){
    accessToken
    refreshToken
    user{
      username
    }
  }
}
     """ 
     response = gql.mutate(mutation)     
     # snapshot.assert_match(response.data)     
     assert response.status_code == 200
     
