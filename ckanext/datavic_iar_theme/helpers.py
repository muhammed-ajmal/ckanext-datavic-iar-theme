import ckan.model as model
import ckan.plugins.toolkit as toolkit
import logging

from ckan.common import config
from sqlalchemy import and_ as _and_
from sqlalchemy.sql import func

log = logging.getLogger(__name__)


def organization_list():
    return toolkit.get_action('organization_list')({}, {'all_fields': True})


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
    except Exception, e:
        log.error(e.message)

    return resource_formats


def get_parent_site_url():
    return config.get('ckan.parent_site_url', 'https://www.data.vic.gov.au')
