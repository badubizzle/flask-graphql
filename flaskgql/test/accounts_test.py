def test_get_user_accounts(client, gql,snapshot):
     mutation = """
     mutation{
          createUser(username: "Badu"){
               user{    
                   uuid                
                   username
               }
          }
     }
     """ 
     response = gql.mutate(mutation)

     mutation = """
     mutation{
          createAccount(username: "Badu"){
              account{
                  owner{
                      username
                  }
              }               
          }
     }
     """ 

     response = gql.mutate(mutation)
     assert response.status_code == 200
     
     query = """
          query {
               allUsers{
                    edges{
                         node{
                              username
                         }
                    }
               }
          }
     """
     response = gql.query(query)
     assert response.status_code == 200
     # snapshot.assert_match(response.json)
 
