from argparse import ArgumentParser, FileType
from getpass import getpass
import re

from vaultenv.reader import VaultReader
from vaultenv.export import export
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
    parser.add_argument("vaultfile")
    return parser.parse_args()


def get_vault_pass(args):
    if args.ask_vault_pass or not args.vault_password_file:
        return getpass("Vault password: ")
    return args.vault_password_file.read().strip()


def get_variables(args):
    vault_file = args.vaultfile
    vault_pass = get_vault_pass(args)
    reader = VaultReader(
        vault_file=vault_file,
        vault_pass=vault_pass.encode("utf-8"),
    )
    return reader.read()


def get_template_string(args):
    if args.template_string:
        return args.template_string

    return Styles.DEFAULT.value


def get_matcher(args):
    if args.matcher:
        return re.compile(args.matcher)
    return None


def get_envvars(variables, args):
    template_string = get_template_string(args)
    matcher = get_matcher(args)
    return export(
        variables=variables,
        template_string=template_string,
        matcher=matcher,
    )


def main():
    # parse user args
    args = parse_args()

    # extract variables from ansible vault
    variables = get_variables(args)

    # convert variables to environment variables
    envvars = get_envvars(variables, args)

    # print to console
    for key, value in envvars.items():
        print(f"export {key}={value}")  # noqa
