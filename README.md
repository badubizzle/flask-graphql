# Flask GraphQL application

1. Authentication with jwt
2. Protected Mutations and Queries
3. Flask migrate

### Running

1. pip install virtualenv
2. virtualenv venv
   3.. source venv/bin/activate
3. pip install -r requirements.txt
4. make db-init
5. make db-migrate
6. make db-upgrade

7. open http://localhost:5000/graphql
