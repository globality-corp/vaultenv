"""
Test settings.

"""
from pkg_resources import resource_filename

from hamcrest import assert_that, equal_to, has_entries, is_

from vaultenv.settings import load_settings


def test_settings():
    path = resource_filename("vaultenv", "tests/settings.cfg")
    assert_that(
        load_settings("foo", path),
        has_entries(
            vault_file="/path/to/vault",
            vault_password_file=None,
            template_string=None,
            matcher=None,
        ),
    )
    assert_that(
        load_settings("bar", path),
        has_entries(
            vault_file="/path/to/vault",
            vault_password_file=None,
            template_string="{{ key }}",
            matcher=None,
        ),
    )


def test_no_settings():
    assert_that(
        load_settings("foo", "/blah"),
        is_(equal_to(dict())),
    )
