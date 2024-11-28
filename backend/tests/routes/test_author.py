from http import HTTPStatus

from tests.conftest import AuthorFactory


async def test_add_author(async_client, user_token):
    response = await async_client.post(
        '/author',
        headers={'Authorization': f'Bearer {user_token}'},
        json={'name': 'test-name'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'name': 'test-name'}


async def test_add_author_already_exists(async_client, user_token, author):
    response = await async_client.post(
        '/author',
        headers={'Authorization': f'Bearer {user_token}'},
        json={'name': author.name},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': f'{author.name} already in MADR.'}


async def test_add_author_not_authenticated(async_client):
    response = await async_client.post(
        '/author',
        json={'name': 'test'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


async def test_author_name_sanitization_schema(async_client, user_token):
    expected_name = 'a name to correct'
    response = await async_client.post(
        '/author',
        headers={'Authorization': f'Bearer {user_token}'},
        json={'name': ' A   NAmE to correct     '},
    )

    assert response.json()['name'] == expected_name


async def test_delete_author(async_client, user_token, author):
    response = await async_client.delete(
        f'/author/{author.id}',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Author deleted from MADR.'}


async def test_delete_author_not_found(async_client, user_token, author):
    response = await async_client.delete(
        '/author/555',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR.'}


async def test_delete_author_not_authenticated(async_client, author):
    response = await async_client.delete(f'/author/{author.id}')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


async def test_update_author(async_client, user_token, author):
    expected_name = 'name updated'
    response = await async_client.patch(
        f'/author/{author.id}',
        headers={'Authorization': f'Bearer {user_token}'},
        json={'name': expected_name},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': author.id, 'name': expected_name}


async def test_update_author_not_found(async_client, user_token, author):
    response = await async_client.patch(
        '/author/555',
        headers={'Authorization': f'Bearer {user_token}'},
        json={'name': 'update'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR.'}


async def test_update_author_not_authenticated(async_client, author):
    response = await async_client.patch(
        '/author/555',
        json={'name': 'update'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


async def test_get_author_by_id(async_client, author):
    response = await async_client.get(f'/author/{author.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': author.id, 'name': author.name}


async def test_get_author_by_id_not_found(async_client, author):
    response = await async_client.get('/author/555')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR.'}


async def test_list_authors_filter_name_should_return_5_authors(
    async_client, async_session
):
    expected_authors = 5
    authors_to_add = AuthorFactory.create_batch(5)
    async_session.add_all(authors_to_add)
    await async_session.commit()

    response = await async_client.get('/author/?name=author')

    assert len(response.json()['authors']) == expected_authors


async def test_list_authors_filter_name_should_return_empty(
    async_client, async_session
):
    async_session.add_all(AuthorFactory.create_batch(5))
    await async_session.commit()

    response = await async_client.get('/author/?name=different name')

    assert response.json()['authors'] == []


async def test_list_authors_filter_name_empty_return_all_authors(
    async_client, async_session
):
    expected_authors = 10
    async_session.add_all(AuthorFactory.create_batch(expected_authors))
    await async_session.commit()

    response = await async_client.get('/author/?name=')

    assert len(response.json()['authors']) == expected_authors


async def test_list_authors_pagination_should_return_20_authors(
    async_session, async_client
):
    expected_books = 20
    async_session.add_all(AuthorFactory.create_batch(25))
    await async_session.commit()

    response = await async_client.get('/author/?name=author')

    assert len(response.json()['authors']) == expected_books
