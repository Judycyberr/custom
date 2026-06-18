{
    'name' : 'Project Management',
    'description' : "Project Management",
    'version' : '19.0.1.0.0',
    'application' : True,
    'category' : 'Project',
    'depends': ['base','project'],
    'data' : [
        'security/ir.model.access.csv',
        'views/project_management_project_task_views.xml',
        'views/project_management_project_task_type_views.xml',
        'views/project_management_menus.xml',
    ]
}