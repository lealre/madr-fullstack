from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, HTTPException

from src.api.dependencies import (
    CurrentUser,
    SessionDep,
)
from src.core.security import (
    create_url_safe_token,
    decode_url_safe_token,
)
from src.email.email import create_email_message, email
from src.schemas.base import Email, Message
from src.schemas.users import (
    PasswordChange,
    UserRequestCreate,
    UserRequestUpdate,
    UserResponse,
)
from src.services import user_service

router = APIRouter()


@router.post(
    '/singup', status_code=HTTPStatus.CREATED, response_model=UserResponse
)
async def singup(session: SessionDep, user_in: UserRequestCreate) -> Any:
    """
    Create an account.
    """

    user_db = await user_service.get_user(
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

    new_user = await user_service.add_user(session=session, user=user_in)

    return new_user


@router.get('/me', response_model=UserResponse)
async def get_user_info_me(current_user: CurrentUser) -> Any:
    """
    Get own account details.
    """

    return current_user


@router.patch('/me', response_model=UserResponse)
async def update_user_info_me(
    session: SessionDep,
    user_in: UserRequestUpdate,
    current_user: CurrentUser,
) -> Any:
    """
    Update own account information.
    """

    user_db = await user_service.get_user(
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

    user_updated = await user_service.update_user_info(
        session=session, user_info=user_in, user_to_update=current_user
    )

    return user_updated


@router.delete('/me', response_model=Message)
async def delete_user_me(
    session: SessionDep, current_user: CurrentUser
) -> Message:
    """
    Delete own account.
    """

    await session.delete(current_user)
    await session.commit()

    return Message(message='User deleted.')


@router.patch('/me/change-password', response_model=Message)
async def update_password_me(
    session: SessionDep,
    passwords: PasswordChange,
    current_user: CurrentUser,
) -> Any:
    """
    Change own password
    """

    if passwords.password != passwords.password_confirmation:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Passwords dont match.'
        )

    await user_service.change_password(
        session=session,
        user_to_update=current_user,
        password=passwords.password,
    )

    return {'message': 'Password has been changed!'}


# -- Email verification routes --


@router.get('/check-verification-status/{user_id}', response_model=Message)
async def is_verified(
    session: SessionDep, current_user: CurrentUser, user_id: int
) -> Message:
    """
    Check if own account is verified.
    """

    user_db = await user_service.get_user_by_id(
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
        return Message(message='User is already verified.')

    return Message(message='User has not been verified yet.')


@router.get('/verify-account', response_model=Message)
async def verify_account(current_user: CurrentUser) -> Message:
    """
    Send an email to the user to verify their account.
    """

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

    return Message(message=f'Email sent to {current_user.email}')


@router.get('/verify/{token}', response_model=Message)
async def verify(
    session: SessionDep, current_user: CurrentUser, token: str
) -> Message:
    """
    Verify the user account based on the verification email sent.
    """

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

    return Message(message='Account verified sucessfully!')


@router.post('/test-email', response_model=Message)
async def test_email(emails: Email) -> Message:
    recipient_email_addresses = emails.addresses
    html = '<h1>Testing Email</h1>'
    message = create_email_message(
        recipients=recipient_email_addresses,
        subject='Welcome to the test',
        body=html,
    )
    await email.send_message(message)

    return Message(message='Email sent')


# -- Email recovery access routes --


@router.get('/recover-access', response_model=Message)
async def recover_access(current_user: CurrentUser) -> Message:
    """
    Recover account access (WIP).
    """

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

    return Message(message=f'Email sent to {current_user.email}')


@router.post('/change-password/{token}', response_model=Message)
async def change_password_by_email(
    session: SessionDep,
    passwords: PasswordChange,
    current_user: CurrentUser,
    token: str,
) -> Message:
    """
    Change password when account recovery is requested (WIP).
    """

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

    await user_service.change_password(
        session=session,
        user_to_update=current_user,
        password=passwords.password,
    )

    return Message(message='Password has been changed!')
