import ckan.model as model
import ckan.plugins.toolkit as toolkit
import logging

from ckan.common import config
from sqlalchemy import and_ as _and_
from sqlalchemy.sql import func
import ckan.lib.helpers as h
import dominate.tags as tags

log = logging.getLogger(__name__)


def organization_list():
    org_list = toolkit.get_action('organization_list')({}, {})
    organizations = []
    for org in org_list:
        org_dict = toolkit.get_action('organization_show')({}, {'id': org})
        organizations.append(org_dict)

    return organizations


def get_parent_orgs(output=None):
    organisations = model.Group.get_top_level_groups('organization')

    if output == 'list':
        parent_orgs = [org.name for org in organisations]
    else:
        parent_orgs = [
            {'value': '', 'text': 'Please select...'}
        ]
        for org in organisations:
            parent_orgs.append({'value': org.name, 'text': org.display_name})

    return parent_orgs


def search_form_group_list():
    return toolkit.get_action('group_list')({}, {'all_fields': True})


def format_list(limit=100):
    resource_formats = []
    try:
        session = model.Session

        query = (session.query(
            model.Resource.format,)
            .filter(_and_(
                model.Resource.state == 'active',
            ))
            .group_by(model.Resource.format)
            .order_by(
                func.lower(model.Resource.format)
            ))
        resource_formats = [resource.format for resource in query if not resource.format == '']
    except Exception as e:
        log.error(e.message)

    return resource_formats


def get_parent_site_url():
    return config.get('ckan.parent_site_url', 'https://www.data.vic.gov.au')


def hotjar_tracking_enabled():
    return toolkit.asbool(config.get('ckan.tracking.hotjar_enabled', False))


def get_hotjar_hsid():
    return config.get('ckan.tracking.hotjar.hjid', None)


def get_hotjar_hjsv():
    return config.get('ckan.tracking.hotjar.hjsv', None)


def get_gtm_code():
    # To get Google Tag Manager Code
    gtm_code = config.get('ckan.google_tag_manager.gtm_container_id', False)
    return str(gtm_code)


def datavic_linked_user(user, maxlength=0, avatar=20):
    # Copied from ckan.lib.helpers.linked_user
    if not isinstance(user, model.User):
        user_name = str(user)
        user = model.User.get(user_name)
        if not user:
            return user_name
    if user:
        name = user.name if model.User.VALID_NAME.match(user.name) else user.id
        displayname = user.display_name

        if maxlength and len(user.display_name) > maxlength:
            displayname = displayname[:maxlength] + '...'

        return h.literal(u'{icon} {link}'.format(
            icon=h.gravatar(
                email_hash=user.email_hash,
                size=avatar
            ),
            link=h.link_to(
                displayname,
                # DataVic custom changes to show different links depending on user access
                h.url_for('user.read', id=name) if h.check_access('package_create') else  h.url_for('user.activity', id=name)
            )
        ))
