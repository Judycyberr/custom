{
    'name' : 'Sale Order Task',
    'description' : "Sale Order Task",
    'version' : '19.0.1.0.0',
    'application' : True,
    'category' : 'sale',
    'depends': ['base','sale'],
    'data' : [
        'security/ir.model.access.csv',
        'views/sale_order_task_views.xml',
        'views/sale_order_project_task_views.xml',
    ]
}