{
    'name' : 'Project Test',
    'description' : "Project Test",
    'version' : '19.0.1.0.0',
    'application' : True,
    'category' : 'pro',
    'depends': ['base','project','analytic','hr_timesheet'],
    'data' : [
        'security/ir.model.access.csv',
        'views/project_project_views.xml',
        'views/project_task_views.xml',
        # 'views/account_analytic_line_views.xml',
    ]
}