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
    get_password_hash,
)
from src.email.email import create_email_message, email
from src.schemas.base import Email, Message
from src.schemas.users import (
    PasswordChange,
    SuperUserRequestCreate,
    SuperUserRequestUpdate,
    UserListResponse,
    UserRequestCreate,
    UserResponse,
)
from src.services import users_service

router = APIRouter()


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

    user = await users_service.get_user_by_id(session=session, user_id=user_id)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )
    if user == current_user:
        raise HTTPException(
            status_code=403,
            detail='Super users are not allowed to delete themselves',
        )

    await session.delete(user)
    await session.commit()

    return {'message': 'User deleted.'}


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


# Users routes
@router.post('/singup', response_model=UserResponse)
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


# User - verify account through email
@router.get('/check-verification-status', response_model=Message)
async def is_verified(current_user: CurrentUser):
    if current_user.is_verified:
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
    emails = emails.addresses
    html = '<h1>Testing Email</h1>'
    message = create_email_message(
        recipients=emails, subject='Welcome to the test', body=html
    )
    await email.send_message(message)

    return {'message': 'Email sent'}


# User - change password through email
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
            detail='Could not proceed with password change.',
        )

    if passwords.password != passwords.password_confirmation:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Passwords doesnt match'
        )

    hashed_password = get_password_hash(passwords.password)
    current_user.password_hash = hashed_password
    session.add(current_user)
    await session.commit()

    return {'message': 'Password changed!'}
