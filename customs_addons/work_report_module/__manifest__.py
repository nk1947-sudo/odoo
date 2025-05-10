{
    'name': 'Advanced Work Report',
    'version': '18.0.1.0',
    'summary': 'Track and manage work reports efficiently',
    'description': """
        Comprehensive module for managing employee work reports,
        exporting to PDF/XLSX, notifications, templates, tags,
        approval workflows, and dashboards.
    """,
    'category': 'Human Resources',
    'author': 'NK',
    'website': 'https://yourcompany.com',
    'depends': [
        'base',
        'mail',
        'hr',
        'project',
        'web',
       # 'report_xlsx',
    ],
    'data': [
        # ✅ Security & Access Control
        'security/work_report_security.xml',
        'security/ir.model.access.csv',


  
        'views/work_report_menu.xml',
        # ✅ Views
        'views/work_report_template_views.xml',

        'views/work_report_line_views.xml',
        'views/work_report_tag_views.xml',
        # 'views/work_report_category_views.xml',  # Optional, leave commented if not used

        # ✅ Data Files
        'data/work_report_data.xml',
        # 'data/work_report_demo.xml',  # Optional demo data

        # ✅ Reports
        'report/work_report_templates.xml',

        # ✅ Main Views
        'views/work_report_views.xml',
       
        # ✅ Extras
        'views/work_report_dashboard.xml',
        'wizard/generate_work_report_wizard_views.xml',
    ],
    'assets': {
    'web.assets_backend': [
        'work_report_module/static/src/js/work_report_dashboard.js',
        'work_report_module/static/src/js/dashboard.js',
        'work_report_module/static/src/js/work_report_widgets.js',
        'work_report_module/static/src/css/work_report.css',
    ],
    'web.assets_qweb': [
        'work_report_module/static/src/xml/dashboard_templates.xml',
    ],
},
    
    'installable': True,
    'application': True,
    'auto_install': False,

    # ✅ Skips enterprise/core tests on Odoo.sh
    'test_tags': ['-enterprise', '-standard'],

    'license': 'AGPL-3',

    # ✅ Make sure the hook is correctly registered and exists in __init__.py
    'post_init_hook': 'post_init_remove_broken_report',

    

}
