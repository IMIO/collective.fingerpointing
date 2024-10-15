# -*- coding: utf-8 -*-
"""Tests for usergroup subscriber."""
from collective.fingerpointing.testing import INTEGRATION_TESTING
from collective.fingerpointing.testing import QIBBB
from logging import INFO
from Products.PluggableAuthService.events import PrincipalAddedToGroup
from Products.PluggableAuthService.events import PrincipalRemovedFromGroup
from testfixtures import LogCapture
from zope.event import notify

import unittest


class UserGroupSubscribersTestCase(unittest.TestCase, QIBBB):
    """Tests for PrincipalAddedToGroup and PrincipalRemovedFromGroup subscribers."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_principal_added_to_group(self):
        event = PrincipalAddedToGroup('test_user_1_', 'bar')
        with LogCapture('collective.fingerpointing', level=INFO) as log:
            notify(event)
            log.check(
                ('collective.fingerpointing', 'INFO', 'user=test_user_1_ ip=None action=added to group principalid=test_user_1_, groupid=bar'),  # noqa: E501
            )

    def test_principal_removed_from_group(self):
        event = PrincipalRemovedFromGroup('test_user_1_', 'bar')
        with LogCapture('collective.fingerpointing', level=INFO) as log:
            notify(event)
            log.check(
                ('collective.fingerpointing', 'INFO', 'user=test_user_1_ ip=None action=removed from group principalid=test_user_1_, groupid=bar'),  # noqa: E501
            )

