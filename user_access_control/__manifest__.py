{
    'name': 'Advanced User Access Control - Customized Access Rights | Record Rules | Fields Restrictions',
    'version': '16.0',
    'summary': """Hide Create/Edit/Delete options, Readonly form, filter records using domain rules,
     and set field-level restrictions.
    Simplify the user Access rights/Access management.""",
    'description': """
        Advanced Access Manager/ Access restriction for Odoo 16
        =====================================
        This module provides control over user access rights management, allowing administrators to precisely configure what users can see and do within the Odoo system.
        - Configure detailed access rights (create/edit/delete/import/export)
        - Set field-level restrictions (readonly/invisible/mandatory)
        - Define record filters using domains
        - Manage three user types with different access levels
        """,
    'author': 'Lambda Digitech',
    'license': 'LGPL-3',
    'category': 'Services',
    'depends': ['web', 'base'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/res_users.xml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'price':  49.99,
    'currency':  'USD',
    'installable': True,
}
