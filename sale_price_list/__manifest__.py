{
    'name' : 'Sale Order Price List',
    'description' : "Sale Order List",
    'version' : '19.0.1.0.0',
    'application' : True,
    'category' : 'sale',
    'depends': ['base','sale'],
    'data' : [
        'security/ir.model.access.csv',
        'views/price_list_views.xml',
        'views/sale_order_price_list_views.xml',
        'views/price_list_menu.xml',
    ]
}