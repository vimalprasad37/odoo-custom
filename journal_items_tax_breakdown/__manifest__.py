# -*- coding: utf-8 -*-
{
    "name" : "Tax Breakdown in Journal Items",
    "version" : "16.0.0.0",
    "category" : "Accounting",
    "description": """
        This Odoo app prevents the same taxes from being grouped together in Journal Items
    """,
    "author": "Lambda Digitech",
    "depends" : ["base","account"],
    "data": [
        "views/account_tax_view.xml"
    ],
    "auto_install": False,
    "installable": True,
    "license": "LGPL-3",
    "images": ["static/description/banner.png"],
    "application":  True,
    "installable":  True
}

