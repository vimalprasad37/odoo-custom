# -*- coding: utf-8 -*-
{
    'name': "Product Stock Sale - Quick Product Selection for Sales Order Lines",
    'summary': """Quickly view available stock, input quantity and price, and add multiple product lines
     to a sales order from a advanced pop-up interface—improving efficiency and accuracy in order processing""",
    'description': """
        This Odoo module streamlines the sales order creation process by allowing users to:
        1.View real-time stock availability (On Hand, Reserved, and Available Quantities) in a tabular format.
        2.Select multiple products, specify quantities, and set prices directly from the stock overview.
        3.Add selected items to sales order lines in bulk via the "ADD LINES" button or individually per line.
        4.Discard selections or save changes effortlessly.
    """,
    "version": "16.0",
    "category": "Sales",
    "author": "Lambda Digitech",
    "images": ["static/description/banner.gif"],
    "depends": ['sale_management', 'web', 'stock'],
    'license': 'LGPL-3',
    "data": [
        'security/ir.model.access.csv',
        'views/sale_view.xml',
        'wizard/stock_sale_popup_view.xml'
    ],
    "assets": {
        "web.assets_backend": [
            "sale_line_product_stock/static/src/css/style.scss",
            "sale_line_product_stock/static/src/js/popup_sale.js"
        ]
    },
    "application": False,
    'installable': True,
}
