"""Tests for password hashing helpers (backend/hash_pswrd.py)."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from hash_pswrd import hash_pswd, verify_pswd  # noqa: E402


def test_hash_is_not_plaintext():
    h = hash_pswd("correct horse battery staple")
    assert h != "correct horse battery staple"
    assert h.startswith("$argon2")


def test_verify_accepts_correct_password():
    h = hash_pswd("s3cret-pass")
    assert verify_pswd("s3cret-pass", h) is True


def test_verify_rejects_wrong_password():
    h = hash_pswd("s3cret-pass")
    assert verify_pswd("wrong-pass", h) is False


def test_hash_is_salted_per_call():
    assert hash_pswd("same") != hash_pswd("same")


def test_verify_returns_false_on_garbage_hash():
    assert verify_pswd("x", "not-a-hash") is False
