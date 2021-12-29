# -*- coding: utf-8 -*-
{
    'name': "time_sheet_module",

    'summary': """
        Module Pointage made by Syrine Riahi""",

    'description': """
        -saisie nom de fiche de pointage
        -select mois et l'année
        -les listes des employées sont chargés automatiquement
        -select les jours present 
        -saisie le cout par jours
        -saisie les avances s'il existe
        -les calcules se fait automatiquement
        
    """,

    'author': "IDVEY",
    'website': "http://www.idvey.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        #'views/hr_timesheet_sheet_templates.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'qweb': ['static/src/xml/timesheet.xml', ],
    #     'js': ['static/src/xml/petstore.js', ],
    #     'qweb': ['static/src/xml/petstore.xml', ],
    #     'qweb': ['static/src/xml/timesheet.xml', ],

}
