from odoo import fields, models,tools, api,_
from odoo.exceptions import ValidationError

import json

class SalesOrder(models.Model):
    _inherit = 'sale.order'

    def action_open_stock(self):
        self._cr.execute("""
            select product_id, lot_id, quantity, reserved_quantity, (quantity - reserved_quantity) as avbl_quantity,
            pt.uom_id as product_uom_id, pt.list_price as sales_price
            from stock_quant sq 
            left join product_product pp on pp.id=sq.product_id
            left join product_template pt on pt.id=pp.product_tmpl_id
            left join stock_location loc on loc.id=sq.location_id
            where loc.usage = 'internal' and pt.sale_ok=true
        """)
        stock_data = self._cr.dictfetchall()
        if stock_data:
            popup_data = self.env['stock.sale.popup'].create(stock_data)
            popup_data.update({
                'sale_id': self.id,
                'user_id': self.env.user.id
            })
            action = self.env['ir.actions.act_window']._for_xml_id('sale_line_product_stock.stock_sale_popup_view')
            action['domain'] = [('id', 'in', popup_data.ids),('user_id', '=', self.env.user.id)]
            return action
