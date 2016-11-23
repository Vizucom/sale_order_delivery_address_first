# -*- coding: utf-8 -*-
from openerp import api, models, fields


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def onchange_partner_id(self, partner_id):

        if self.env.context.get('called_first', False) == 'partner_delivery_id':
            print "Partner onchange called, but from delivery. Popping shipping_id..."
            res = super(SaleOrder, self).onchange_partner_id(partner_id)
            # Don't suggest delivery address based on the partner
            res['value'].pop('partner_shipping_id', None)
            return res
        else:
            print "Partner onchange called, calling super as usual..."
            res = super(SaleOrder, self.with_context(called_first='partner_id')).onchange_partner_id(partner_id)
            return res

        """
        # onchange_delivery_id is also called from code inside onchange_partner_id.
        # use a context parameter so that these calls can be ignored in the method
        res = super(SaleOrder, self.with_context(skip_delivery_onchange=True)).onchange_partner_id(partner_id)

        # Don't suggest delivery address based on the partner
        res['value'].pop('partner_shipping_id', None)
        return res
        """

    @api.multi
    def onchange_delivery_id(self, company_id, partner_id, delivery_id, fiscal_position):

        print "Onchange delivery reached, calling super..."

        if self.env.context.get('called_first', False) == 'partner_id':
            print "Delivery onchange was reached from partner_onchange. Returning res..."
            res = super(SaleOrder, self).onchange_delivery_id(company_id, partner_id, delivery_id, fiscal_position)
            # return super(SaleOrder, self).onchange_delivery_id(company_id, partner_id, delivery_id, fiscal_position)
            return res
        else:
            print "Delivery onchange was not reached from partner_onchange but called initially. Setting main partner to be delivery's parent, or falling back to delivery itself..."
            # res = super(SaleOrder, self.with_context(called_first='partner_delivery_id')).onchange_delivery_id(company_id, partner_id, delivery_id, fiscal_position)
            res = super(SaleOrder, self.with_context(called_first='partner_delivery_id')).onchange_delivery_id(company_id, partner_id, delivery_id, fiscal_position)

            if delivery_id:
                # Suggest partner baesd on the delivery address
                delivery_partner = self.env['res.partner'].browse(delivery_id)
                res['value']['partner_id'] = delivery_partner.parent_id and delivery_partner.parent_id.id or delivery_id

            return res

        """
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
        """
