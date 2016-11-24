# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2016- Vizucom Oy (http://www.vizucom.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Sale Order: Delivery Address First',
    'category': 'Sale',
    'version': '0.1',
    'author': 'Vizucom Oy',
    'website': 'http://www.vizucom.com',
    'depends': ['sale', 'web_context_tunnel'],
    'description': """
Sale Order: Delivery Address First
==================================
 * Modifies the Sale Order form so that setting the delivery address first suggests the parent partner
 * Depends on OCA's web_context_tunnel module (https://github.com/OCA/server-tools/tree/8.0/web_context_tunnel)

    """,
    'data': [
        'views/sale_order.xml',
    ],
}
