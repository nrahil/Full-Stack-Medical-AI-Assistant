import os
import pytest
import sqlite3
import tempfile
from unittest.mock import patch

from chat_history import (
    create_session,
    get_sessions,
    get_session,
    update_session_title,
    update_session_document,
    add_message,
    get_messages,
    delete_session,
    init_db
)

@pytest.fixture(autouse=True)
def isolated_db(tmp_path, monkeypatch):
    """Use a temporary SQLite database for each test to avoid polluting state."""
    temp_db = str(tmp_path / "test_chat.db")
    monkeypatch.setattr("chat_history.DB_PATH", temp_db)
    init_db()
    yield temp_db
    if os.path.exists(temp_db):
        os.remove(temp_db)


def test_create_and_get_session():
    user_id = "user_test_123"
    session = create_session(user_id=user_id, title="Test Consultation", active_document="report.pdf")
    
    assert session["id"] is not None
    assert session["user_id"] == user_id
    assert session["title"] == "Test Consultation"
    assert session["active_document"] == "report.pdf"

    retrieved = get_session(session["id"])
    assert retrieved is not None
    assert retrieved["title"] == "Test Consultation"


def test_update_session_meta():
    session = create_session(user_id="user_test_456", title="Original Title")
    session_id = session["id"]

    update_session_title(session_id, "Updated Medical Consultation")
    update_session_document(session_id, "blood_test_results.pdf")

    updated = get_session(session_id)
    assert updated["title"] == "Updated Medical Consultation"
    assert updated["active_document"] == "blood_test_results.pdf"


def test_add_and_retrieve_messages():
    session = create_session(user_id="user_test_789", title="Chat Session")
    session_id = session["id"]

    msg1 = add_message(session_id, "user", "What do high WBC counts indicate?")
    msg2 = add_message(session_id, "ai", "High WBC may indicate infection or inflammation.")

    messages = get_messages(session_id)
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert "WBC" in messages[0]["content"]
    assert messages[1]["role"] == "ai"


def test_delete_session_cascades():
    session = create_session(user_id="user_test_999", title="Session to Delete")
    session_id = session["id"]
    add_message(session_id, "user", "Hello")

    delete_session(session_id)
    assert get_session(session_id) is None
    assert get_messages(session_id) == []
