
from dotenv import load_dotenv
from unittest.mock import Mock
import pytest

from ..src import db_repository as repo
from ..src.model.hobby import Hobby
from mysql.connector import Error
from ..src.model.model import Model
from ..src.db import Db

load_dotenv()

def make_mocks():
    # Create mock connection and cursor with the methods used
    cursor = Mock()
    connection = Mock()
    connection.cursor.return_value = cursor
    return connection, cursor


def test_insert_hobby_builds_correct_query_and_commits(monkeypatch):
    connection, cursor = make_mocks()
    monkeypatch.setattr(repo, "Db", type("_D", (), {"connect": staticmethod(lambda: connection)}))

    # Given a Hobby model; note: Hobby.to_tuple returns (user_id, name, satisfaction_level, hability, time)
    hobby = Hobby(user_id=1, name="Chess", satisfaction_level=5, hability="medium", time=2.5)

    # When calling insert
    repo.insert(None, hobby, db="akali_hobby")

    # Then it should prepare SQL and execute with the tuple from model
    assert cursor.execute.call_count == 1
    sql, params = cursor.execute.call_args[0]

    # Check SQL targets correct database and table and has 5 placeholders
    assert "INSERT INTO akali_hobby.hobby" in sql
    assert sql.count("%s") == 5

    # Ensure params are the model tuple as provided
    assert params == hobby.to_tuple()

    # Commit and clean-up
    connection.commit.assert_called_once()
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


def test_insert_hobby_propagates_error(monkeypatch):
    connection, cursor = make_mocks()
    monkeypatch.setattr(repo, "Db", type("_D", (), {"connect": staticmethod(lambda: connection)}))

    # Make execute raise an Error-like exception
    class DummyError(Exception):
        pass

    cursor.execute.side_effect = DummyError("DB error")

    hobby = Hobby(user_id=2, name="Running", satisfaction_level=4, hability="high", time=1.0)

    with pytest.raises(DummyError):
        repo.insert(None, hobby, db="akali_hobby")


def test_selectAll_returns_rows_list(monkeypatch):
    connection, cursor = make_mocks()
    # Ensure cursor(dictionary=True) returns our cursor regardless of parameter
    def cursor_with_dict(dictionary=False):
        return cursor
    connection.cursor.side_effect = cursor_with_dict
    monkeypatch.setattr(repo, "Db", type("_D", (), {"connect": staticmethod(lambda: connection)}))

    # Prepare mocked fetchall result
    rows = [
        {"id": 1, "user_id": 1, "name": "Chess", "satisfaction_level": 5, "hability": "medium", "time": 2.5},
        {"id": 2, "user_id": 2, "name": "Running", "satisfaction_level": 4, "hability": "high", "time": 1.0},
    ]
    cursor.fetchall.return_value = rows

    result = repo.selectAll(None)

    cursor.execute.assert_called_once()
    assert cursor.execute.call_args[0][0].strip().lower().startswith("select * from hobby")
    assert result == rows
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


def test_delete_uses_table_from_db_param_bug_documented(monkeypatch):
    """
    The current delete() implementation uses f"DELETE FROM {db} WHERE id = %s" (missing table).
    This test documents current behavior: it should attempt to execute using the provided db string as table spec.
    If later fixed to include .hobby, this test can be updated accordingly.
    """
    connection, cursor = make_mocks()
    monkeypatch.setattr(repo, "Db", type("_D", (), {"connect": staticmethod(lambda: connection)}))

    repo.delete(None, id=42, db="akali_hobby.hobby")

    cursor.execute.assert_called_once()
    sql, params = cursor.execute.call_args[0]
    assert sql.startswith("DELETE FROM akali_hobby.hobby")
    assert params == (42,)
    connection.commit.assert_called_once()
    cursor.close.assert_called_once()
    connection.close.assert_called_once()
