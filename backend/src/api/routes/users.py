from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from src.core.security import (
    create_url_safe_token,
    decode_url_safe_token,
)
from src.email.email import create_email_message, email
from src.schemas.base import Email, Message
from src.schemas.users import (
    PasswordChange,
    SuperUserRequestCreate,
    SuperUserRequestUpdate,
    UserListResponse,
    UserRequestCreate,
    UserRequestUpdate,
    UserResponse,
)
from src.services import users_service

router = APIRouter()


# -- Superuser routes --


@router.get(
    '/all',
    response_model=UserListResponse,
    dependencies=[Depends(get_current_active_superuser)],
)
async def read_users(session: SessionDep, limit: int = 100, offset: int = 0):
    """
    Superuser - Retrieve all user accounts.
    """

    users = await users_service.get_users_list(
        session=session, offset=offset, limit=limit
    )

    return {'users': users}


@router.get(
    '/{user_id}',
    response_model=UserResponse,
    dependencies=[Depends(get_current_active_superuser)],
)
async def get_user_by_id(session: SessionDep, user_id: int):
    """
    Superuser - Get account by ID.
    """

    user_db = await users_service.get_user_by_id(
        session=session, user_id=user_id
    )

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )

    return user_db


@router.post(
    '/',
    response_model=UserResponse,
    status_code=HTTPStatus.CREATED,
    dependencies=[Depends(get_current_active_superuser)],
)
async def create_user(session: SessionDep, user_in: SuperUserRequestCreate):
    """
    Superuser - Create a user account.
    """

    user_db = await users_service.get_user(
        session=session, user_email=user_in.email, username=user_in.username
    )

    if user_db:
        if user_db.username == user_in.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists.',
            )
        if user_db.email == user_in.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists.',
            )

    new_user = await users_service.add_user(session=session, user=user_in)

    return new_user


@router.patch(
    '/{user_id}',
    response_model=UserResponse,
    dependencies=[Depends(get_current_active_superuser)],
)
async def update_user_info(
    session: SessionDep, user_id: int, user_in: SuperUserRequestUpdate
):
    """
    Superuser - Update a user's account info.
    """

    user_to_update = await users_service.get_user_by_id(
        session=session, user_id=user_id
    )

    if not user_to_update:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )

    user_db = await users_service.get_user(
        session=session, username=user_in.username, user_email=user_in.email
    )

    if user_db:
        if user_db.username == user_in.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists.',
            )
        if user_db.email == user_in.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists.',
            )

    user_updated = await users_service.update_user_info(
        session=session, user_info=user_in, user_to_update=user_to_update
    )

    return user_updated


@router.delete(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    dependencies=[Depends(get_current_active_superuser)],
)
async def delete_user(
    session: SessionDep, user_id: int, current_user: CurrentUser
):
    """
    Superuser - Delete a user account by ID.
    """

    user_to_delete = await users_service.get_user_by_id(
        session=session, user_id=user_id
    )

    if not user_to_delete:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )
    if user_to_delete.id == current_user.id:
        raise HTTPException(
            status_code=403,
            detail='Super users are not allowed to delete themselves',
        )

    await session.delete(user_to_delete)
    await session.commit()

    return {'message': 'User deleted.'}


# -- Users routes --


@router.post(
    '/singup', status_code=HTTPStatus.CREATED, response_model=UserResponse
)
async def singup(session: SessionDep, user_in: UserRequestCreate):
    """
    User - Create an account.
    """

    user_db = await users_service.get_user(
        session=session, user_email=user_in.email, username=user_in.username
    )

    if user_db:
        if user_db.username == user_in.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists.',
            )
        if user_db.email == user_in.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists.',
            )

    new_user = await users_service.add_user(session=session, user=user_in)

    return new_user


@router.get('/me/{user_id}', response_model=UserResponse)
async def get_user_info_me(user_id: int, current_user: CurrentUser):
    """
    User - Get own account details by ID.
    """

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions.'
        )

    return current_user


@router.patch('/me/{user_id}', response_model=UserResponse)
async def update_user_info_me(
    session: SessionDep,
    user_id: int,
    user_in: UserRequestUpdate,
    current_user: CurrentUser,
):
    """
    User - Update own account information by ID.
    """

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions.'
        )

    user_db = await users_service.get_user(
        session=session, username=user_in.username, user_email=user_in.email
    )

    if user_db:
        if user_db.username == user_in.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists.',
            )
        if user_db.email == user_in.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists.',
            )

    user_updated = await users_service.update_user_info(
        session=session, user_info=user_in, user_to_update=current_user
    )

    return user_updated


@router.delete('/me/{user_id}', response_model=Message)
async def delete_user_me(
    session: SessionDep, user_id: int, current_user: CurrentUser
):
    """
    User - Delete own account.
    """

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions.'
        )

    await session.delete(current_user)
    await session.commit()

    return {'message': 'User deleted.'}


@router.patch('/me/change-password/{user_id}', response_model=Message)
async def update_password_me(
    session: SessionDep,
    user_id: int,
    passwords: PasswordChange,
    current_user: CurrentUser,
):
    """
    User - Change own password
    """

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions.'
        )

    if passwords.password != passwords.password_confirmation:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Passwords dont match.'
        )

    await users_service.change_password(
        session=session,
        user_to_update=current_user,
        password=passwords.password,
    )

    return {'message': 'Password has been changed!'}


# -- Email verification routes --


@router.get('/check-verification-status/{user_id}', response_model=Message)
async def is_verified(
    session: SessionDep, current_user: CurrentUser, user_id: int
):
    """
    User - Check if own account is verified.
    """

    user_db = await users_service.get_user_by_id(
        session=session, user_id=user_id
    )

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions.'
        )

    if user_db.is_verified:
        return {'message': 'User is already verified.'}

    return {'message': 'User has not been verified yet.'}


@router.get('/verify-account/', response_model=Message)
async def verify_account(current_user: CurrentUser):
    email_token = create_url_safe_token(data={'email': current_user.email})

    link = f'http://127.0.0.1:8000/users/verify/{email_token}'

    html_message = f"""
        <h1>Verify your account</h1>
        <p>Click in this <a href={link}>link</a> to verify your account </p>
    """

    message = create_email_message(
        recipients=[current_user.email],
        subject='Verify your email',
        body=html_message,
    )

    await email.send_message(message)

    return {'message': f'Email sent to {current_user.email}'}


@router.get('/verify/{token}')
async def verify(session: SessionDep, current_user: CurrentUser, token: str):
    email_token = decode_url_safe_token(token)

    if not email_token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Could not validate credentials.',
        )

    user_email = email_token.get('email')

    if not user_email or user_email != current_user.email:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Could not validate account',
        )

    user_updated = current_user
    user_updated.is_verified = True
    session.add(user_updated)
    await session.commit()

    return {'message': 'Account verified sucessfully!'}


@router.post('/test-email', response_model=Message)
async def test_email(emails: Email):
    emails = emails.addresses  # type: ignore
    html = '<h1>Testing Email</h1>'
    message = create_email_message(
        recipients=emails,  # type: ignore
        subject='Welcome to the test',
        body=html,  # type: ignore
    )
    await email.send_message(message)

    return {'message': 'Email sent'}


# -- Email recovery access routes --


@router.get('/recover-access')
async def recover_access(current_user: CurrentUser):
    email_token = create_url_safe_token(data={'email': current_user.email})

    link = f'http://127.0.0.1:8000/users/change-password/{email_token}'

    html_message = f"""
        <h1>Reset Password</h1>
        <p>Click in this <a href={link}>link</a> to reset your password</p>
    """

    message = create_email_message(
        recipients=[current_user.email],
        subject='Reset Password',
        body=html_message,
    )

    await email.send_message(message)

    return {'message': f'Email sent to {current_user.email}'}


@router.post('/change-password/{token}')
async def change_password_by_email(
    session: SessionDep,
    passwords: PasswordChange,
    current_user: CurrentUser,
    token: str,
):
    email_token = decode_url_safe_token(token)

    if not email_token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Could not validate credentials.',
        )

    user_email = email_token.get('email')

    if not user_email or user_email != current_user.email:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Password change could not be completed.',
        )

    if passwords.password != passwords.password_confirmation:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Passwords dont match.'
        )

    await users_service.change_password(
        session=session,
        user_to_update=current_user,
        password=passwords.password,
    )

    return {'message': 'Password has been changed!'}
