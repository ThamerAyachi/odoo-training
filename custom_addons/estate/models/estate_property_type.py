# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class EstatePropertyType(models.Model):
    """Estate Property Type Class"""

    _name = "estate.property.type"
    _description = "Type of estate property"

    name = fields.Char(required=True)
