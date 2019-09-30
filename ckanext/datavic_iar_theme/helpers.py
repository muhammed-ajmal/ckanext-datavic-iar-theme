import ckan.model as model
import ckan.plugins.toolkit as toolkit

from ckan.common import config
from sqlalchemy import and_ as _and_

def organization_list():
    return toolkit.get_action('organization_list')({}, {'all_fields': True})


def search_form_group_list():
    return toolkit.get_action('group_list')({}, {'all_fields': True})


def format_list(limit=100):
    session = model.Session

    query = (session.query(
        model.Resource.format,)
        .filter(_and_(
            model.Resource.state == 'active',
        ))
        .group_by(model.Resource.format)
        .order_by('format ASC'))

    return [resource.format for resource in query if not resource.format == '']

def get_parent_site_url():
    return config.get('ckan.parent_site_url', 'https://www.data.vic.gov.au/')
