# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from unittest import TestCase
from pyup.config import Config, RequirementConfig, CompileConfig


class ConfigTestCase(TestCase):

    def test_repr(self):
        config = Config()
        self.assertEqual(config.__repr__(), str(config.__dict__))

    def test_defaults(self):
        config = Config()
        self.assertEqual(config.close_prs, True)
        self.assertEqual(config.branch, "master")
        self.assertEqual(config.pin, True)
        self.assertEqual(config.search, True)
        self.assertEqual(config.requirements, [])
        self.assertEqual(config.schedule, "")

    def test_pin_file(self):
        config = Config()
        config.requirements = [
            RequirementConfig(path="foo.txt", pin=False)
        ]

        self.assertEqual(config.pin_file("foo.txt"), False)

        config.pin = False
        config.requirements[0].pin = True

        self.assertEqual(config.pin_file("foo.txt"), True)

        self.assertEqual(config.pin_file("other.txt"), False)

    def test_update(self):
        update = {
            "branch": "some branch",
            "requirements": [
                "foo.txt",
                {"bar.txt": {"pin": True, "compile": {"specs": ["baz.in", "foo.in"]}}}
            ]
        }
        config = Config()
        self.assertEqual(config.requirements, [])
        self.assertEqual(config.branch, "master")

        config.update(update)

        self.assertEqual(config.branch, "some branch")
        self.assertEqual(config.requirements[0].path, "foo.txt")
        self.assertEqual(config.requirements[1].path, "bar.txt")
        self.assertEqual(config.requirements[2].path, "baz.in")
        self.assertEqual(config.requirements[3].path, "foo.in")
        self.assertEqual(config.requirements[1].pin, True)
        self.assertEqual(config.requirements[1].compile.specs, ["baz.in", "foo.in"])


class RequirementConfigTestCase(TestCase):

    def test_repr(self):
        config = RequirementConfig(path="foo.txt")
        self.assertEqual(config.__repr__(), str(config.__dict__))


class CompileConfigTestCase(TestCase):

    def test_repr(self):
        config = CompileConfig()
        self.assertEqual(config.__repr__(), str(config.__dict__))

    def test_default(self):
        config = CompileConfig()
        self.assertEqual(config.specs, [])
