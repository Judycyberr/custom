{
    'name' : 'Customer Product',
    'description' : "Customer Product",
    'version' : '19.0.1.0.0',
    'application' : True,
    'category' : 'cus',
    'depends': ['base','product'],
    'data' : [
        'security/ir.model.access.csv',
        'views/customer_partner_views.xml',
        'views/product_template_views.xml',
    ]
}