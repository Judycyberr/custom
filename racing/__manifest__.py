{
    'name': 'Racing',
    'application': True,
    'version': '1.0',
    'category': 'Race',
    'depends': [
        'base','event','hr','mass_mailing_event','stock'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/race_team_management.xml',
    ]

}