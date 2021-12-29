# -*- coding: utf-8 -*-
{
    'name': 'Tunisia_account.14',
    'version': '1.0',
    'author': 'SMART2DOTECH',
    'website': 'http://www.smart2tech.com',
    'summary': 'Manage Chart of Accounts and Taxes template for companies in Tunisia with odoo 14',
    'category': 'Localization/Account Charts',
    'description': """
      This is the base module to manage Chart of Accounts and Taxes template for companies in Tunisia.
      Ce Module charge le modèle du plan de comptes standard Tunisien et permet de générer les états
      comptables aux normes tunisiennes.""",
    'depends': ['base_iban', 'account', 'base_vat'],
    'init_xml': [],
    'data': [
        'data/tn_pcg_taxes.xml',
        'data/plan_comptable_general.xml',
        'data/tn_tax.xml',
        'data/tn_fiscal_templates.xml',
        #add on migration
        'data/account_chart_template.xml',
        # 'data/account_chart_template.yml',
        
    ],
    'images': [
        'images/wct_tn.png',
    ],
    'test': [],
    'demo_xml': [],
    # 'active': True,
    'installable': True,
}
