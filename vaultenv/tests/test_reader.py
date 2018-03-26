"""
Test vault reading.

"""
from pathlib import PurePath
from pkg_resources import resource_filename

from hamcrest import assert_that, has_entries

from vaultenv.reader import VaultReader


class TestVaultReader:

    def test_read(self):
        vault_file = PurePath(resource_filename("vaultenv", "tests/vault.yml"))
        vault_pass = "secret".encode("utf-8")
        reader = VaultReader(
            vault_file=vault_file,
            vault_pass=vault_pass,
        )

        contents = reader.read()
        assert_that(contents, has_entries(
            foo="bar",
            bar="baz",
            baz="foo",
        ))
