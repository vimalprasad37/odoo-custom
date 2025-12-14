from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class StockSalePopup(models.TransientModel):
    _name = 'stock.sale.popup'
    _description = "Detailed stock info for all the products"

    sale_id = fields.Many2one('sale.order', string="Sales Order")
    user_id = fields.Many2one('res.users', string="User")
    product_id = fields.Many2one('product.product', string='Product', required=True)
    lot_id = fields.Many2one('stock.lot', string='Lot/Serial No')
    quantity = fields.Float(string='On Hand Qty', help="Total stock quantity including reserved stocks")
    reserved_quantity = fields.Float(string='Reserved Qty', help="Quantities reserved on other orders/deliveries")
    avbl_quantity = fields.Float(string='Available Qty', help="Actual quantity available to deliver")
    product_uom_id = fields.Many2one('uom.uom', string="UOM")
    sales_qty = fields.Float(string='Quantity to sell', help="Enter the quantity for the product to add in Sales Order Line.", default=1)
    sales_price = fields.Float(string='Price to sell', help="Enter the price for the product to add in Sales Order Line.")
    sale_line_updated = fields.Boolean("Updated in Sale line?")

    @api.onchange('sales_qty', 'sales_price')
    def _onchange_sales_qty(self):
        for rec in self:
            current_rec = self.browse(rec._origin.id)
            current_rec.write({'sale_line_updated': True, 'sales_qty': rec.sales_qty, 'sales_price': rec.sales_price})

    def add_multi_sale_lines(self):
        active_ids = self._context.get('active_ids', False)
        if active_ids:
            for rec in self.browse(active_ids):
                vals = {
                    'order_id': rec.sale_id.id,
                    'product_id' : rec.product_id.id,
                    'product_uom_qty' : rec.sales_qty,
                    'price_unit': rec.sales_price,
                    'product_uom': rec.product_uom_id.id,
                }
                order_line = self.env['sale.order.line'].create(vals)
                order_line._onchange_product_id_warning()
            return True

    def add_to_sale_line(self):
        self.ensure_one()
        vals = {
            'order_id': self.sale_id.id,
            'product_id' : self.product_id.id,
            'product_uom_qty' : self.sales_qty,
            'price_unit': self.sales_price,
            'product_uom': self.product_uom_id.id,
        }
        order_line = self.env['sale.order.line'].create(vals)
        order_line._onchange_product_id_warning()
        return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'success',
                    'message': _(f'Product "{self.product_id.display_name}" with quantity {self.sales_qty} added to Sales order line.'),
                }
            }