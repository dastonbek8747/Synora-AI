"""Tests for request/response models (backend/schemas_models.py)."""

import os
import sys

import pytest
from pydantic import ValidationError

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from schemas_models import CreateUser, LoginUser, PatchUser  # noqa: E402


def test_create_user_ok():
    u = CreateUser(
        username="doston",
        email="doston@example.com",
        password="supersecret",
        confirm_password="supersecret",
    )
    assert u.username == "doston"


def test_create_user_password_mismatch():
    with pytest.raises(ValidationError):
        CreateUser(
            username="doston",
            email="doston@example.com",
            password="supersecret",
            confirm_password="different",
        )


def test_create_user_rejects_short_password():
    with pytest.raises(ValidationError):
        CreateUser(
            username="doston",
            email="doston@example.com",
            password="short",
            confirm_password="short",
        )


def test_create_user_rejects_bad_email():
    with pytest.raises(ValidationError):
        CreateUser(
            username="doston",
            email="not-an-email",
            password="supersecret",
            confirm_password="supersecret",
        )


def test_login_user_requires_fields():
    with pytest.raises(ValidationError):
        LoginUser(username="doston")


def test_patch_user_all_fields_optional():
    assert PatchUser().username is None
