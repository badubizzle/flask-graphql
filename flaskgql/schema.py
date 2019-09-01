from .middleware import timing_middleware
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy

from .query import Query
from .mutation import Mutation


import graphene

schema = graphene.Schema(query=Query, mutation=Mutation)

def init_app(app):
    
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            middleware=[],
            graphiql=True,  # for having the GraphiQL interface,

        )
    )