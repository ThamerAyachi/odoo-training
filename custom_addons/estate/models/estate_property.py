# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    """Estate Property Class"""

    _name = "estate.property"
    _description = "Estate Property Class Description"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Datetime.now()+relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    seller_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False, string="Bayer")
    estate_property_tag_ids = fields.Many2many(
        'estate.property.tag', string="Tags")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offer")
    total_area = fields.Float(
        compute="_compute_total_area", readonly=True, string="Total Area (sqm)")
    best_price = fields.Float(
        compute="_compute_best_price", readonly=True, string="Best Offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        """Function to calculate Total Area"""
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        """Function to Find Best Price"""
        for record in self:
            offer_price = record.offer_ids.mapped('price')
            if not offer_price:
                record.best_price = None
            else:
                record.best_price = max(offer_price)

    @api.onchange("garden", "garden_area", "garden_orientation")
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = None
            self.garden_orientation = None
        else:
            self.garden_area = 10
            self.garden_orientation = "north"
