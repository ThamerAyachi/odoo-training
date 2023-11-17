# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from datetime import date, datetime, timedelta


class EstatePropertyOffer(models.Model):
    """Estate Property Offer Class"""

    _name = "estate.property.offer"
    _description = "Offer for estate property"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ]
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer('Validity (days)', default=7)
    create_date = fields.Date('Create Date')
    date_deadline = fields.Date(
        'Deadline', compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = None
            else:
                record.date_deadline = record.create_date + \
                    timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = None
            if not record.date_deadline:
                record._compute_deadline()
            else:
                validity_1 = record.date_deadline-record.create_date
                record.validity = validity_1.days

    def action_accept(self):
        for offer in self.property_id.offer_ids:
            if offer.status == "accepted":
                raise UserError("Another offer have been accepted!")
        self.status = "accepted"
        self.property_id.state = 'offer_accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id

    def action_refuse(self):
        self.status = "refused"
