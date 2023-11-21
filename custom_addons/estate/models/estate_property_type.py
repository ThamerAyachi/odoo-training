# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class EstatePropertyType(models.Model):
    """Estate Property Type Class"""

    _name = "estate.property.type"
    _description = "Type of estate property"
    _order = "sequence, name desc"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer(
        default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer("offer_count", compute='_compute_offers')

    _sql_constraints = [
        (
            "check_name",
            "UNIQUE(name)",
            "A property name must be unique"
        )
    ]

    @api.depends('offer_ids')
    def _compute_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
