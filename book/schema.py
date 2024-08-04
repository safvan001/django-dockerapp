import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from book.models import Book
from django.contrib.auth.models import User 
from book.serializer import Userserializer, Bookserializer
from django.contrib.auth import authenticate
from graphql_jwt.shortcuts import get_token, create_refresh_token
import graphql_jwt


class UserType(DjangoObjectType):
    class Meta:
        model = User

class BookType(DjangoObjectType):
    class Meta:
        model = Book

# Define GraphQL Queries
class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)
    book = graphene.Field(BookType, id=graphene.ID(required=True))

    def resolve_all_books(self, info):
        return Book.objects.all()

    def resolve_book(self, info, id):
        return Book.objects.get(pk=id)

# Define GraphQL Mutations
class SignUp(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        return SignUp(user=user)

class UserLogin(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    message = graphene.String()

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            return UserLogin(message="Authentication failed")
        return UserLogin(message="Authentication Successful")

class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        author_id = graphene.ID(required=True)  # Foreign key to User
        price = graphene.Int(required=True)

    book = graphene.Field(BookType)

    def mutate(self, info, title, description, author_id, price):
        author = User.objects.get(pk=author_id)
        book = Book.objects.create(title=title, description=description, author=author, price=price)
        return CreateBook(book=book)

class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()
        price = graphene.Int()

    book = graphene.Field(BookType)

    def mutate(self, info, id, title=None, description=None, price=None):
        book = Book.objects.get(pk=id)
        if title:
            book.title = title
        if description:
            book.description = description
        if price:
            book.price = price
        book.save()
        return UpdateBook(book=book)

class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        book = Book.objects.get(pk=id)
        book.delete()
        return DeleteBook(success=True)

# Define the schema
class Mutation(graphene.ObjectType):
    sign_up = SignUp.Field()
    user_login = UserLogin.Field()
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
