# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError, UserError, ValidationError


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
        default='new',
        readonly=True
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

    def action_cancel(self):
        if self.state == "sold":
            raise UserError("Sold Properties can't be canceled!")
        else:
            self.state = "canceled"

    def action_sold(self):
        if self.state == "canceled":
            raise UserError("Canceled Properties can't be sold!")
        else:
            self.state = "sold"

    _sql_constraints = [
        (
            'check_expected_price',
            'CHECK(expected_price > 0)',
            'A property expected price must be strictly positive'
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "A property selling price must be positive"
        ),
        (
            "check_name",
            "UNIQUE(name)",
            "A property name must be Unique"
        )
    ]
