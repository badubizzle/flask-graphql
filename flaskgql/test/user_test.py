
def test_get_all_users(client, gql,snapshot):
     
     query = """
          query {
               allUsers{
                    edges{
                         node{
                              uuid
                         }
                    }
               }
          }
     """
     response = gql.query(query)
     assert response.status_code == 200
     # snapshot.assert_match(response.json)


def test_create_user_with_user_name(client,gql, snapshot):

     mutation = """
     mutation{
          createUser(username: "Badu"){
               user{                    
                    username
               }
          }
     }
     """ 
     response = gql.mutate(mutation)     
     # snapshot.assert_match(response.data)     
     assert response.status_code == 200
     
