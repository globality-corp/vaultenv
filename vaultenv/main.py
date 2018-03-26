from argparse import ArgumentParser, FileType
from getpass import getpass
from os.path import expanduser
import re

from vaultenv.reader import VaultReader
from vaultenv.export import export
from vaultenv.settings import load_settings
from vaultenv.styles import Styles


def parse_args():
    parser = ArgumentParser()

    # format
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--default", dest="template_string", action="store_const", const=Styles.DEFAULT.value)
    group.add_argument("--identity", dest="template_string", action="store_const", const=Styles.IDENTITY.value)
    group.add_argument("-tf", "--terraform", dest="template_string", action="store_const", const=Styles.TERRAFORM.value)
    group.add_argument("-t", "--template-string")

    # variable matching
    parser.add_argument("-m", "--matcher")

    # ansible vault
    parser.add_argument("--ask-vault-pass", action="store_true")
    parser.add_argument("--vault-password-file", type=FileType("r"))
    parser.add_argument(dest="vault_file", help="vaultfile path or settings key name")
    return parser.parse_args()


def get_vault_pass(args, settings):
    if not args.ask_vault_pass:
        if args.vault_password_file:
            return args.vault_password_file.read().strip()
        if settings.get("vault_password_file"):
            with open(expanduser(settings["vault_password_file"])) as file_:
                return file_.read().strip()

    return getpass("Vault password: ")


def get_variables(args, settings):
    vault_file = settings.get("vault_file") or args.vault_file
    vault_pass = get_vault_pass(args, settings)
    reader = VaultReader(
        vault_file=vault_file,
        vault_pass=vault_pass.encode("utf-8"),
    )
    return reader.read()


def get_template_string(args, settings):
    if args.template_string:
        return args.template_string

    if settings.get("template_string"):
        return settings["template_string"]

    return Styles.DEFAULT.value


def get_matcher(args, settings):
    if args.matcher:
        return re.compile(args.matcher)
    if settings.get("matcher"):
        return re.compile(settings["matcher"])
    return None


def get_envvars(variables, args, settings):
    template_string = get_template_string(args, settings)
    matcher = get_matcher(args, settings)
    return export(
        variables=variables,
        template_string=template_string,
        matcher=matcher,
    )


def main():
    # parse user args
    args = parse_args()

    # load settings from config file
    settings = load_settings(args.vault_file)

    # extract variables from ansible vault
    variables = get_variables(args, settings)

    # convert variables to environment variables
    envvars = get_envvars(variables, args, settings)

    # print to console
    for key, value in envvars.items():
        print(f"export {key}={value}")  # noqa
