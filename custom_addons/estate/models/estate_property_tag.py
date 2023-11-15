# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class EstatePropertyTag(models.Model):
    """Estate Property Tag Class"""

    _name = "estate.property.tag"
    _description = "Tag of estate property"

    name = fields.Char(required=True)
