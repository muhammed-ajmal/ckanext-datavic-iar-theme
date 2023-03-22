from __future__ import annotations

import logging
from typing import Optional, Any

from sqlalchemy.sql import func

import ckan.model as model
import ckan.plugins.toolkit as tk
import ckan.lib.helpers as h

from ckanext.toolbelt.decorators import Collector

import ckanext.datavic_iar_theme.config as conf


log = logging.getLogger(__name__)
helper, get_helpers = Collector("vic_iar").split()


@helper
def organization_list() -> list[dict[str, Any]]:
    return tk.get_action("organization_list")(
        {}, {"all_fields": True, "include_dataset_count": False}
    )


@helper
def get_parent_orgs(output: Optional[str] = None) -> list[dict[str, str]] | list[str]:
    organisations: list[model.Group] = model.Group.get_top_level_groups("organization")

    if output == "list":
        parent_orgs = [org.name for org in organisations]
    else:
        parent_orgs = [{"value": "", "text": "Please select..."}]
        for org in organisations:
            parent_orgs.append({"value": org.name, "text": org.display_name})

    return parent_orgs


@helper
def search_form_group_list() -> list[dict[str, Any]]:
    return tk.get_action("group_list")(
        {}, {"all_fields": True, "include_dataset_count": False}
    )


@helper
def format_list() -> list[str]:
    """Return a list of all available resources on portal"""

    query = (
        model.Session.query(model.Resource.format)
        .filter(model.Resource.state == model.State.ACTIVE)
        .group_by(model.Resource.format)
        .order_by(func.lower(model.Resource.format))
    )

    return [resource.format for resource in query if resource.format]


@helper
def get_parent_site_url():
    return conf.get_parent_site_url()


@helper
def hotjar_tracking_enabled():
    return conf.hotjar_tracking_enabled()


@helper
def get_hotjar_hsid():
    return conf.get_hotjar_hsid()


@helper
def get_hotjar_hjsv():
    return conf.get_hotjar_hjsv()


@helper
def get_gtm_container_id():
    return conf.get_gtm_container_id()


@helper
def linked_user(user: str, maxlength: int = 0, avatar: int = 20):
    """Custom linked_user helper"""
    user_obj: model.User | None = model.User.get(user)

    if not user_obj:
        return user

    name: str = (
        user_obj.name if model.User.VALID_NAME.match(user_obj.name) else user_obj.id
    )
    display_name = user_obj.display_name

    if maxlength and len(user_obj.display_name) > maxlength:
        display_name = display_name[:maxlength] + "..."

    # DataVic custom changes to show different links depending on user access
    url: str = (
        h.url_for("user.read", id=name)
        if h.check_access("package_create")
        else h.url_for("activity.user_activity", id=name),
    )  # type: ignore

    return h.literal(
        "{icon} {link}".format(
            icon=h.gravatar(email_hash=user_obj.email_hash, size=avatar),
            link=h.link_to(display_name, url),
        )
    )


@helper
def visibility_list() -> list[dict[str, str]]:
    return [
        {"value": "all", "label": "Open to the public and VPS only"},
        {"value": "private", "label": "Open to VPS only"},
        {"value": "public", "label": "Open to the public"},
    ]


@helper
def featured_resource_preview(package: dict[str, Any]) -> Optional[dict[str, Any]]:
    """Return a featured resource preview if exists for a specific dataset"""
    featured_preview = None
    if package.get("nominated_view_id", None):
        try:
            resource_view = tk.get_action("resource_view_show")(
                {}, {"id": package["nominated_view_id"]}
            )
            resource = tk.get_action("resource_show")(
                {}, {"id": resource_view["resource_id"]}
            )
            featured_preview = {"preview": resource_view, "resource": resource}
        except tk.ObjectNotFound:
            pass
    return featured_preview
