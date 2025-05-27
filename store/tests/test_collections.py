
from store.models import Collection, Products
from model_bakery import baker
from rest_framework import status
import pytest

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return  api_client.post('/store/collections/', collection)
    return do_create_collection

@pytest.mark.django_db
class TestCreateCollection:
    #to skip a test we use @pytest.mark.skip
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        #Arrange

        #Act
        response = create_collection({'title': 'a'})

        #Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_401(self, api_client, create_collection, auth_usr):
        #Arrange
        auth_usr()

        #Act
        response = create_collection({'title': 'b'})

        #Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, api_client, create_collection, auth_usr):
        #Arrange
        auth_usr(is_staff=True)

        #Act
        response = create_collection({'title': ''})

        #Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, api_client, create_collection, auth_usr):
        #Arrange
        auth_usr(is_staff=True)

        #Act
        response = create_collection({'title': 'c'})

        #Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db #to enable access to the db
class TestRetrieveCollection:
    def test_if_collection_exits_returns_200(self, api_client):
        #Arrange
        collection = baker.make(Collection) #Read the doc for more info on how to use the bakery library
        # baker.make(Products, collection=collection, _quantity=10) #creates just 10 products and puts them in the same collection specified

        #Action
        response = api_client.get(f'/store/collections/{collection.id}/')

        #Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 0,
            'featured_product': None
        }

#Create tests for the collections endpoints and products endpoints