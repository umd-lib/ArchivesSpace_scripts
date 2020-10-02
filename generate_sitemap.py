#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as et

from asnake.aspace import ASpace
import asnake.logging as logging

# Gather configuration
api_baseurl = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
public_baseurl = sys.argv[4]

config = {'baseurl': api_baseurl,
          'username': username,
          'password': password,
          'default_config': 'INFO_TO_STDERR'}

aspace = ASpace(**config)

logger = logging.get_logger("sitemap")
logger.info(f'config={config}')

# Authorize as the provided username
aspace.authorize()

# Start the xml output
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'

urlset = et.Element(et.QName(NS, 'urlset'))
doc = et.ElementTree(urlset)

# Add the homepage
url = et.SubElement(urlset, et.QName(NS, 'url'))
loc = et.SubElement(url, et.QName(NS, 'loc'))
loc.text = f'{public_baseurl}/'
url.tail = '\n'

# Iterate over published repositories
for repo in aspace.repositories:
    if repo.publish:

        url = et.SubElement(urlset, et.QName(NS, 'url'))
        loc = et.SubElement(url, et.QName(NS, 'loc'))
        loc.text = f'{public_baseurl}{repo.uri}'
        url.tail = '\n'

        logger.info(f'{repo.uri} {repo.display_string}')

        # Iterate over published resources
        for resource in repo.resources:
            if resource.publish and not resource.suppressed:
                url = et.SubElement(urlset, et.QName(NS, 'url'))
                loc = et.SubElement(url, et.QName(NS, 'loc'))
                loc.text = f'{public_baseurl}{resource.uri}'
                url.tail = '\n'

                logger.info(f'{resource.uri} {resource.title}')

        # Iterate over published digital objects
        for digital_object in repo.digital_objects:
            if digital_object.publish:
                url = et.SubElement(urlset, et.QName(NS, 'url'))
                loc = et.SubElement(url, et.QName(NS, 'loc'))
                loc.text = f'{public_baseurl}{digital_object.uri}'
                url.tail = '\n'

                logger.info(f'{digital_object.uri} {digital_object.title}')

# Write the XML Sitemap to stdout
doc.write(sys.stdout,
          encoding='unicode',
          xml_declaration=True,
          default_namespace=NS)
