"""Test command line utilities."""

from . import tmp_cli_runner  # NOQA


def test_cli_register_user(tmp_cli_runner):  # NOQA
    from dtool_lookup_server.utils import _get_user_obj

    assert _get_user_obj("admin") is None

    from dtool_lookup_server.cli import register_user

    result = tmp_cli_runner.invoke(register_user, ["--is_admin", "admin"])
    assert result.exit_code == 0

    new_user = _get_user_obj("admin")
    expected_content = {
        "username": "admin",
        "is_admin": True,
        "search_permissions_on_base_uris": [],
        "register_permissions_on_base_uris": []
    }
    assert new_user.as_dict() == expected_content

    tmp_cli_runner.invoke(register_user, ["dopey"])
    new_user = _get_user_obj("dopey")
    expected_content = {
        "username": "dopey",
        "is_admin": False,
        "search_permissions_on_base_uris": [],
        "register_permissions_on_base_uris": []
    }
    assert new_user.as_dict() == expected_content

    result = tmp_cli_runner.invoke(register_user, ["dopey"])
    assert result.exit_code != 0
    assert "User 'dopey' already registered" in result.output


def test_cli_register_base_uri(tmp_cli_runner):  # NOQA
    from dtool_lookup_server.utils import _get_base_uri_obj

    b_uri = "s3://snow-white"
    assert _get_base_uri_obj(b_uri) is None

    from dtool_lookup_server.cli import add_base_uri

    result = tmp_cli_runner.invoke(add_base_uri, [b_uri])
    assert result.exit_code == 0

    new_base_uri = _get_base_uri_obj(b_uri)
    expected_content = {
        "base_uri": b_uri,
        "users_with_search_permissions": [],
        "users_with_register_permissions": []
    }
    assert new_base_uri.as_dict() == expected_content


def test_cli_give_search_permission(tmp_cli_runner):  # NOQA

    from dtool_lookup_server.utils import (
        _get_base_uri_obj,
        register_users,
        register_base_uri,
    )

    username1 = "sleepy"
    username2 = "dopey"
    base_uri_str = "s3://snow-white"
    register_users([{"username": username1}, {"username": username2}])
    register_base_uri(base_uri_str)

    from dtool_lookup_server.cli import give_search_permission

    result = tmp_cli_runner.invoke(
        give_search_permission,
        [base_uri_str, username1])
    assert result.exit_code == 0

    base_uri = _get_base_uri_obj(base_uri_str)
    expected_content = {
        "base_uri": base_uri_str,
        "users_with_search_permissions": [username1],
        "users_with_register_permissions": []
    }
    assert base_uri.as_dict() == expected_content

    result = tmp_cli_runner.invoke(
        give_search_permission,
        [base_uri_str, username2])
    assert result.exit_code == 0

    base_uri = _get_base_uri_obj(base_uri_str)
    expected_content = {
        "base_uri": base_uri_str,
        "users_with_search_permissions": [username1, username2],
        "users_with_register_permissions": []
    }
    assert base_uri.as_dict() == expected_content

    result = tmp_cli_runner.invoke(
        give_search_permission,
        [base_uri_str, username2])
    assert result.exit_code != 0
    assert "User '{}' already has search permissions".format(username2) in result.output  # NOQA

    result = tmp_cli_runner.invoke(
        give_search_permission,
        ["s3://no-uri", "dopey"])
    assert result.exit_code != 0
    assert "Base URI 's3://no-uri' not registered" in result.output

    result = tmp_cli_runner.invoke(
        give_search_permission,
        [base_uri_str, "noone"])
    assert result.exit_code != 0
    assert "User 'noone' not registered" in result.output


def test_cli_give_register_permission(tmp_cli_runner):  # NOQA

    from dtool_lookup_server.utils import (
        _get_base_uri_obj,
        register_users,
        register_base_uri,
    )

    username1 = "sleepy"
    username2 = "dopey"
    base_uri_str = "s3://snow-white"
    register_users([{"username": username1}, {"username": username2}])
    register_base_uri(base_uri_str)

    from dtool_lookup_server.cli import give_register_permission

    result = tmp_cli_runner.invoke(
        give_register_permission,
        [base_uri_str, username1])
    assert result.exit_code == 0

    base_uri = _get_base_uri_obj(base_uri_str)
    expected_content = {
        "base_uri": base_uri_str,
        "users_with_search_permissions": [],
        "users_with_register_permissions": [username1]
    }
    assert base_uri.as_dict() == expected_content

    result = tmp_cli_runner.invoke(
        give_register_permission,
        [base_uri_str, username2])
    assert result.exit_code == 0

    base_uri = _get_base_uri_obj(base_uri_str)
    expected_content = {
        "base_uri": base_uri_str,
        "users_with_search_permissions": [],
        "users_with_register_permissions": [username1, username2]
    }
    assert base_uri.as_dict() == expected_content

    result = tmp_cli_runner.invoke(
        give_register_permission,
        [base_uri_str, username2])
    assert result.exit_code != 0
    assert "User '{}' already has register permissions".format(username2) in result.output  # NOQA

    result = tmp_cli_runner.invoke(
        give_register_permission,
        ["s3://no-uri", "dopey"])
    assert result.exit_code != 0
    assert "Base URI 's3://no-uri' not registered" in result.output

    result = tmp_cli_runner.invoke(
        give_register_permission,
        [base_uri_str, "noone"])
    assert result.exit_code != 0
    assert "User 'noone' not registered" in result.output