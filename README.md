# vaultenv

Ansible vault environment variable exporting.

CLI interface to export Ansible vault values as environment variables.


## Setup

Use `vaultenv` with a virtualenv (e.g. using `virtualenv-wrapper`):

    mkvirtualenv vaultenv

For normal usage, install from PyPi:

    pip install vaultenv

For development, install test requirements and local source:

    pip install nose PyHamcrest
    pip install -e .

Then, run the `vaultenv` CLI:

    vaultenv --help


## Usage


At its simplest, `vaultenv` takes the path to an Ansible vault file and prompts for the vault password:

    # Run vaultenv using the test vault (which uses the password "secret")
    vaultenv ./vaultenv/tests/vault.yml

As with other Ansible vault operations, `vaultenv` also accepts a password file:

    echo "secret" > /tmp/vault-pass.txt
    vaultenv --vault-password-file /tmp/vault-pass.txt ./vaultenv/tests/vault.yml

In the likely event that the vault contains more variables than necessary, use a regex matcher:

    vaultenv --matcher "^b" --vault-password-file /tmp/vault-pass.txt ./vaultenv/tests/vault.yml

To control the output format, use a Jinaj2 template string:

    vaultenv --template-string "{{ key | lower }}" --matcher "^b" --vault-password-file /tmp/vault-pass.txt ./vaultenv/tests/vault.yml

Some format styles are built-in:

    vaultenv --terraform --matcher "^b" --vault-password-file /tmp/vault-pass.txt ./vaultenv/tests/vault.yml


## Settings

Default values for commonly used options can be written to `~/.vaultenv` using config format:

    [production]
    vault_file = /path/to/vault
    vault_password_file = /path/to/vault_password_file
    template_string = TF_VAR_{{ key }}
    matcher = ^log

Then, simply use the section name as the vault file path:

    vaultenv production

In this form, it will likely be useful to `eval` the outcome:

    eval "$(vaultenv production)"
