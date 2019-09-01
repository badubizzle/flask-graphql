CREATE_ACCOUNT_MUTATION = """
          mutation{{
           createAccount(username: "{0}", token:"{1}"){{
              account{{
              ... on AccountObject{{
                uuid
                balance
              }}
              ... on AuthInfoField{{
                    message
              }}
            }}
          }}
          }}
     """
DEPOSIT_MUTATION = """
     mutation{{
       depositMoney(accountUuid:"{0}", amount: {2}, token:"{1}"){{
         account{{
           ... on AccountObject{{
             balance
             uuid
           }}
           ... on AuthInfoField{{
             message
           }}
         }}
       }}
     }}
     """

WITHDRAW_MUTATION = """
    mutation{{
      withdrawMoney(accountUuid:"{0}", amount: {2}, token:"{1}"){{
        account{{
          ... on AccountObject{{
            balance
            uuid
          }}
          ... on AuthInfoField{{
            message
          }}
        }}
      }}
    }}
    """

CREATE_USER_MUTATION = """
     mutation{{
          createUser(username: "{0}"){{
          accessToken
          refreshToken
          user{{
               username
          }}
          }}
     }}
     """
def test_create_accounts(client, gql, snapshot):

    response = gql.mutate(CREATE_USER_MUTATION.format("Kwaku"))
    assert response.status_code == 200
    user = response.json['data']['createUser']
    token = user['accessToken']
    username = user['user']['username']

    response = gql.mutate(CREATE_ACCOUNT_MUTATION.format(username, token))
    assert response.status_code == 200

    # snapshot.assert_match(response.json)


def test_deposit_money(client, gql, snapshot):
    response = gql.mutate(CREATE_USER_MUTATION.format("Kwame"))
    assert response.status_code == 200
    user = response.json['data']['createUser']
    token = user['accessToken']
    username = user['user']['username']

    response = gql.mutate(CREATE_ACCOUNT_MUTATION.format(username, token))
    assert response.status_code == 200
    account = response.json['data']['createAccount']['account']
    print(account)
    assert 'uuid' in account
    assert 'balance' in account
    assert account['balance'] == 0



    account_id = account['uuid']
    print("DEPOSIT===>", DEPOSIT_MUTATION.format(account_id, token, 100))
    print(account_id)
    response = gql.mutate(DEPOSIT_MUTATION.format(account_id, token, 100))

    assert response.status_code == 200
    print(response.json)
    updated_account = response.json['data']['depositMoney']['account']
    assert 'uuid' in updated_account
    assert updated_account['uuid'] == account['uuid']
    assert 'balance' in updated_account
    assert updated_account['balance'] == 100

    # snapshot.assert_match(response.json)

def test_withdraw_money(client, gql, snapshot):

    response = gql.mutate(CREATE_USER_MUTATION.format("Kojo"))
    assert response.status_code == 200
    user = response.json['data']['createUser']
    token = user['accessToken']
    username = user['user']['username']

    response = gql.mutate(CREATE_ACCOUNT_MUTATION.format(username, token))
    assert response.status_code == 200
    account = response.json['data']['createAccount']['account']
    assert 'uuid' in account
    assert 'balance' in account
    assert account['balance'] == 0



    account_id = account['uuid']
    response = gql.mutate(DEPOSIT_MUTATION.format(account_id, token, 100))

    assert response.status_code == 200
    updated_account = response.json['data']['depositMoney']['account']
    assert 'uuid' in updated_account
    assert updated_account['uuid'] == account['uuid']
    assert 'balance' in updated_account
    assert updated_account['balance'] == 100


    response = gql.mutate(WITHDRAW_MUTATION.format(account_id, token, 20))

    assert response.status_code == 200
    updated_account = response.json['data']['withdrawMoney']['account']
    assert 'uuid' in updated_account
    assert updated_account['uuid'] == account['uuid']
    assert 'balance' in updated_account
    assert updated_account['balance'] == 80

