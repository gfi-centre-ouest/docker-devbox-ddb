# -*- coding: utf-8 -*-
from marshmallow import fields

from ddb.feature.schema import FeatureSchema


class TraefikSchema(FeatureSchema):
    """
    Traefik feature schema.
    """
    certs_directory = fields.String(required=False, allow_none=True, default=None)
    config_directory = fields.String(required=False, allow_none=True, default=None)
    mapped_certs_directory = fields.String(required=True, default="/certs")
    ssl_config_template = fields.String(required=True, default="""
# This configuration file has been automatically generated by ddb
[[tls.certificates]]
  certFile = "{{_local.certFile}}"
  keyFile = "{{_local.keyFile}}"
""".lstrip())
