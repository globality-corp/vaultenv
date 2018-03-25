# vaultenv

Ansible vault environment variable exporting.

CLI interface to export Ansible vault values as environment variables.


## Setup

Install `vaultenv` into a virtualenv (e.g. using `virtualenv-wrapper`):

    mkvirtualenv vaultenv
    pip install nose PyHamcrest
    pip install -e .

Then, run the `vaultenv` CLI:

    vaultenv --help


## Usage

    vaultenv /path/to/vaultfile
