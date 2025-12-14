from odoo import fields, models, api, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import ValidationError

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    access_management_ids = fields.One2many('access.management.line', 'user_id', string="Access Management") 
            
class AccessManagementLine(models.Model):
    _name = 'access.management.line'
    _description = "Manage Access rights (Create, Edit, Delete and More) with ease."

    user_id = fields.Many2one('res.users', string="User", ondelete="cascade", index=True)
    model_id = fields.Many2one('ir.model', "Model")
    model_name = fields.Char(related="model_id.model", string="Model Name")
    related_model_ids = fields.Many2many('ir.model', 'ir_models_access_management_rel', string="Related Models", compute="_compute_related_models", store=True)
    user_type = fields.Selection([('user_own', 'User - Own Documents'),
    ('user_all', 'User - All Documents'), ('admin', 'Admin')],
        help="User - Own Documents (Can Access their own records only)\n \
            User - All Documents (Can View and Modify all the records except Deleting)\n \
            Admin (Full access to view, modify or delete all the records)",
        string="User Type", required=True)
    readonly = fields.Boolean("Readonly")
    filter_domain = fields.Char(
        string='Records Filter',
        help="Based on given domain conditions, records will be filtered for this user."
    )
    hide_create = fields.Boolean("Hide Create")
    hide_edit = fields.Boolean("Hide Edit")
    hide_delete = fields.Boolean("Hide Delete")
    hide_export = fields.Boolean("Hide Export")
    hide_import = fields.Boolean("Hide Import", help="Import option cannot be hidden if 'Create' option is disabled")
    fields_restiction = fields.Boolean("Field(s) Restriction?", help="Enable this and scroll down to make any fields Invisible, Readonly or Mandatory.")
    fields_access_ids = fields.One2many('fields.access', 'line_id', string="Fields Access")

    @api.depends('model_id')
    def _compute_related_models(self):
        for rec in self:
            fields = self.env['ir.model.fields']
            model_list = []
            if rec.model_id:
                model_list.append(rec.model_id.id)
                relation_fields = rec.model_id.field_id.filtered(lambda x: x.relation_field )
                if relation_fields:
                    res_field = fields.search([('name', 'in', relation_fields.mapped('relation_field')), ('relation', '=', rec.model_id.model)])
                    if res_field:
                        model_list += res_field.mapped('model_id.id')
            else:
                model_list = [(5, 0, 0)]
            rec.related_model_ids = model_list

    @api.constrains('filter_domain')
    def _validate_domain(self):
        for rec in self:
            if rec.filter_domain:
                try:
                    safe_eval(rec.filter_domain)
                except Exception as e:
                    raise ValidationError(_(str(e)))

    @api.onchange('readonly')
    def _onchange_readonly(self):
        for rec in self:
            rec.hide_create = rec.hide_delete = rec.hide_edit = rec.hide_import = rec.readonly

    @api.onchange('user_type', 'model_id')
    def _onchange_user_type(self):
        for rec in self:
            if rec.user_type != 'admin':
                rec.hide_delete = True
            else:
                 rec.hide_create = rec.hide_delete = rec.hide_edit = rec.hide_import = rec.readonly = False
                    
class FieldsAccess(models.Model):
    _name = 'fields.access'
    _description = "Field Level Access Restrictions"

    line_id = fields.Many2one('access.management.line', string="User", ondelete="cascade", index=True)
    field_ids = fields.Many2many('ir.model.fields', 'ir_model_fields_access_rel',  string="Field Name", required=True)
    restriction_type = fields.Selection([('invisible', 'Invisible/Hide'), ('readonly', 'Readonly'), ('required', 'Mandatory')],
        help="Invisible - Hides the field\n \
            Readonly - Can't change value for the field \n \
            Mandatory - Value must be present for the field",
        string="Restriction Type", required=True)