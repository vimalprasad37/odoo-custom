from odoo import fields, models

class AccountTax(models.Model):
    _inherit = 'account.tax'

    restrict_grouping = fields.Boolean(string="Restrict Grouping ?", help="By enabling, it will prevent this tax from grouping in Journal Items.")