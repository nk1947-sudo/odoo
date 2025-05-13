
{
    "name": "Dawell Tender Pro",
    "summary": "AI-powered Government Tender Management System",
    "version": "1.0.0",
    "category": "Purchases/Tenders",
    "author": "Shaurya Infotech",
    "website": "https://shauryainfotech.com",
    "license": "LGPL-3",
    "depends": ["base",
                 "mail", 
                 "web", 
                 #"documents", 
                 "portal"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/ir_cron_data.xml",
        "data/tender_stage_data.xml",
        "data/email_templates.xml",
        "views/menu.xml",
        "views/tender_views.xml",
        "views/bid_views.xml",
        "views/department_views.xml",
        "views/portal_sync_views.xml",
        "views/ai_insight_views.xml",
        "views/assets.xml",
        "report/tender_summary.xml",
        "report/report_template.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "/tender_pro/static/src/css/tender_dashboard.css",
            "/tender_pro/static/src/js/tender_dashboard.js",
        ]
    },
    "installable": True,
    "application": True,
    "auto_install": False
}