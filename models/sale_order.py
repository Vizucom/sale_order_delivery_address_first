# -*- coding: utf-8 -*-
from openerp import api, models, fields


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def onchange_partner_id(self, partner_id):
        # onchange_delivery_id is also called from code inside onchange_partner_id.
        # use a context parameter so that these calls can be ignored in the method
        res = super(SaleOrder, self.with_context(skip_delivery_onchange=True)).onchange_partner_id(partner_id)

        # Don't suggest delivery address based on the partner
        res['value'].pop('partner_shipping_id', None)
        return res

    @api.multi
    def onchange_delivery_id(self, company_id, partner_id, delivery_id, fiscal_position):

        if self.env.context.get('skip_delivery_onchange', False):
            return {
                'value': {}
            }

        res = super(SaleOrder, self).onchange_delivery_id(company_id, partner_id, delivery_id, fiscal_position)

        if delivery_id:
            # Suggest partner baesd on the delivery address
            delivery_partner = self.env['res.partner'].browse(delivery_id)
            res['value']['partner_id'] = delivery_partner.parent_id and delivery_partner.parent_id.id or False
        else:
            res['value']['partner_id'] = False

        return res
