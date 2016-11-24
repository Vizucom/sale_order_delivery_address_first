# -*- coding: utf-8 -*-
from openerp import api, models, fields


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def onchange_partner_id(self, partner_id):

        res = super(SaleOrder, self).onchange_partner_id(partner_id)

        if self._context.get('shipping_trigger', False):
            # Delivery Address field triggered the change originally, so
            # don't let partner_onchange override the user's selection
            res['value'].pop('partner_shipping_id')

        return res


    @api.multi
    def onchange_delivery_id(self, company_id, partner_id, delivery_id, fiscal_position):

        res = super(SaleOrder, self).onchange_delivery_id(company_id, partner_id, delivery_id, fiscal_position)

        if self._context.get('shipping_trigger', False):
            # Delivery Address field triggered the change originally, so
            # fetch its parent to be the Customer. Or if there is no parent, suggest the address itself.
            if delivery_id:
                delivery_partner = self.env['res.partner'].browse(delivery_id)
                res['value']['partner_id'] = delivery_partner.parent_id and delivery_partner.parent_id.id or delivery_id

        return res
