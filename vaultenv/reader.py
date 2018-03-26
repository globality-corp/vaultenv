from os.path import expanduser, exists

from ansible.parsing.vault import VaultLib, VaultSecret
from yaml import load, SafeLoader


class VaultReader:
    """
    Read data from a vault file.

    """
    def __init__(self, vault_file, vault_pass):
        """
        Create a vault reader.

        :param vault_file: path to an ansible vault file
        :param vault_pass: the vault file's password as bytes

        """
        if not exists(expanduser(vault_file)):
            raise Exception(f"No such file: {vault_file}")
        if not isinstance(vault_pass, bytes):
            raise Exception("Vault pass must be instance of `bytes`")

        self.vault_file = vault_file
        self.vault_pass = vault_pass

    @property
    def secrets(self):
        return dict(
            default=VaultSecret(self.vault_pass),
        )

    def read(self):
        """
        Read vault data as a Python dictionary.

        """
        with open(expanduser(self.vault_file), "rb") as vault_file:
            encrypted = vault_file.read()

        vault_lib = VaultLib(self.secrets.items())
        plaintext = vault_lib.decrypt(encrypted, filename=self.vault_file)
        return load(plaintext, Loader=SafeLoader)
