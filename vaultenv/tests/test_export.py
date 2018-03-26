"""
Test exporting.

"""
import re

from hamcrest import assert_that, has_entries

from vaultenv.export import export
from vaultenv.styles import Styles


class TestExport:

    def setup(self):
        self.variables = dict(
            foo="bar",
            bar="baz",
            baz="foo",
        )

    def test_export_identity(self):
        assert_that(
            export(self.variables, Styles.IDENTITY.value),
            has_entries(
                foo="bar",
                bar="baz",
                baz="foo",
            ),
        )

    def test_export_default(self):
        assert_that(
            export(self.variables, Styles.DEFAULT.value),
            has_entries(
                FOO="bar",
                BAR="baz",
                BAZ="foo",
            ),
        )

    def test_export_terraform(self):
        assert_that(
            export(self.variables, Styles.TERRAFORM.value),
            has_entries(
                TF_VAR_foo="bar",
                TF_VAR_bar="baz",
                TF_VAR_baz="foo",
            ),
        )

    def test_export_with_matcher(self):
        matcher = re.compile("^b")

        assert_that(
            export(self.variables, Styles.DEFAULT.value, matcher),
            has_entries(
                BAR="baz",
                BAZ="foo",
            ),
        )
