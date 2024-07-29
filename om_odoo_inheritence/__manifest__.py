# -*- coding: utf-8 -*-
{
    'name': "om_odoo_inheritence",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Jihed Ha",
    'website': "https://www.facebook.com/profile.php?id=100079998342788",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['sale'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/sale_order_view.xml',
        'views/account_move_view.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
