# -*- coding: utf-8 -*-
from collective.fingerpointing.config import AUDIT_MESSAGE
from collective.fingerpointing.interfaces import IFingerPointingSettings
from collective.fingerpointing.logger import log_info
from collective.fingerpointing.utils import get_request_information
from plone import api
from Products.PluggableAuthService.interfaces.events import IPrincipalAddedToGroupEvent
from Products.PluggableAuthService.interfaces.events import IPrincipalRemovedFromGroupEvent
from zope.component import ComponentLookupError


def usergroup_logger(event):
    """Log log events like user group modification """
    name = IFingerPointingSettings.__identifier__ + '.audit_user_group_attribution'
    try:
        audit_user_group_attribution = api.portal.get_registry_record(name, default=False)
    except ComponentLookupError:  # Plone site removed
        return

    if not audit_user_group_attribution:
        return

    user, ip = get_request_information()

    if IPrincipalAddedToGroupEvent.providedBy(event):
        action = 'added to group'
    elif IPrincipalRemovedFromGroupEvent.providedBy(event):
        action = 'removed from group'
    else:  # should never happen
        action = '-'

    extras = 'principalid={0}, groupid={1}'.format(event.object, event.group_id)
    log_info(AUDIT_MESSAGE.format(user, ip, action, extras))
