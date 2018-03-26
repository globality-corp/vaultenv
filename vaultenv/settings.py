from os.path import expanduser, exists
from configparser import SafeConfigParser


DEFAULT_CONFIG_PATH = "~/.vaultenv"

CONFIG_KEYS = dict(
    vault_file=True,
    vault_password_file=False,
    template_string=False,
    matcher=False,
)


def load_settings(name, path=DEFAULT_CONFIG_PATH):
    if not exists(expanduser(path)):
        return dict()

    parser = SafeConfigParser()
    parser.read(expanduser(path))

    return {
        key: parser.get(name, key) if required else parser.get(name, key, fallback=None)
        for key, required in CONFIG_KEYS.items()
    }
