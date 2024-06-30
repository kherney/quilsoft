# -*- coding: utf-8 -*-
{
    'name': "Vertical Hospital",
    'summary': "Hospital Management for patient for vertical hospital",
    'description': """Hospital Management for patient for vertical hospital""",
    'icon': '/account/static/description/l10n.png',

    'author': "Kevin Rodriguez",
    'contributors': "kevinh@gmail.com",
    'website': "https://github.com/kherney",
    'maintainer': 'kevinh@gmail.com',

    # Categories can be used to filter modules in modules listing
    'category': 'Human Resources',
    'license': 'AGPL-3',
    'version': '17.0',

    'external_dependencies': {},
    'depends': ['web', 'mail'],
    'countries': ['co'],

    # always loaded
    'data': [
        # Security
        'security/ir_groups.xml',
        'security/ir.model.access.csv',
        # Models Views
        'views/hospital_patient_view.xml',
        'views/hospital_treatment_view.xml',
        'views/res_config_setting.xml',
        # Wizard Views
        # Web Templates
        # Report Templates
        'reports/template_list_patient.xml',
        # Data
        'data/ir_sequence.xml',
        # Menus
        'views/menu_views.xml',

    ],
    'assets': {},
    # only loaded in demonstration mode
    'demo': [],

    'auto_install': False,
    'application': False,
    'installable': True,
}
