from ckan.common import config


def get_parent_site_url():
    return config.get('ckan.parent_site_url', 'https://www.data.vic.gov.au/')
