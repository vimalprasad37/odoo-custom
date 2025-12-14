from odoo import models, api, _ 
from odoo.tools.safe_eval import safe_eval
from lxml import etree

class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        user = self.env.user
        if not self._context.get('access_management_rule') and user and not self.env.is_superuser():
            model = self._name
            access = self.env['access.management.line'].sudo().with_context(access_management_rule=True).search([('user_id', '=', user.id),('model_name', '=', model)])
            for rec in access:
                # Adding Domain filter for records
                if rec.user_type == 'user_own':
                    user_field = rec.model_id.field_id.filtered(lambda x: x.name == 'user_id')
                    if user_field:
                        domain += [('user_id', '=', user.id)]
                    else:
                        domain += [('create_uid', '=', user.id)]
                # Adding Domain filter for records
                if rec.filter_domain and rec.filter_domain != '[]':
                    filter_dom = safe_eval(rec.filter_domain)
                    # Removing the duplicate domains if any
                    for dom in domain:
                        if dom in filter_dom:
                            filter_dom.remove(dom)
                    if filter_dom:
                        domain += filter_dom

        return super(Base, self)._search(domain, offset, limit, order, count=count, access_rights_uid=access_rights_uid)
    
    @api.model
    def get_views(self, views, options=None):
        res = super().get_views(views, options=options)
        if res.get('views') and not self.env.is_superuser():
            for view_type, values in res['views'].items():
                if view_type in ('list', 'form'):
                    node = etree.fromstring(values['arch'])
                    model = values['model']
                    user = self.env.user
                    if node is not None and model and user:
                        readonly_access = self.env['access.management.line'].sudo().search([('user_id', '=', user.id),('model_id.model', '=', model), ('readonly', '=', True)])
                        if readonly_access:
                            # Remove all action menu items for Readonly
                            values['toolbar']['action'] = []
        return res

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super(Base, self)._get_view(view_id, view_type, **options)
        user = self.env.user
        access = self.env['access.management.line'].sudo().search([('user_id', '=', user.id),('model_id.model', '=', view.model)])
        if access and arch is not None:
            for rec in access:
                export_group = self.env.ref('base.group_allow_export', False)
                if rec.hide_export:
                    export_group.sudo().write({'users': [(3, self.env.user.id)]})
                else:
                    export_group.sudo().write({'users': [(4, self.env.user.id)]})
                if view_type in ('form', 'tree'):
                    if rec.readonly:
                        for btn in arch.xpath("//header/button"):
                            btn.set('invisible', '1')

                    if rec.fields_restiction:
                        for obj in rec.fields_access_ids:
                            for field in obj.field_ids:
                                for x in arch.xpath("//field[@name='%s']" % field.name):
                                    x.set(obj.restriction_type, "1")

                                if obj.restriction_type == 'invisible' and view_type == 'form':
                                    for l in arch.xpath("//label[@for='%s']" % field.name):
                                        parent = l.getparent()
                                        if parent is not None:
                                            parent.remove(l)
                                            if parent.tag == 'div':
                                                parent.getparent().remove(parent)
                                                

                if view_type != 'search':
                    # Disabling/Enabling Create, Edit, Delete and Import options based on given inputs
                    can_create = '0' if rec.hide_create else '1'
                    can_edit = '0' if rec.hide_edit else '1'
                    can_delete = '0' if rec.hide_delete else '1'
                    can_import = '0' if rec.hide_import else '1'

                    arch.set('create', can_create)
                    arch.set('edit', can_edit)
                    arch.set('delete', can_delete)
                    arch.set('import', can_import)

        return arch, view
