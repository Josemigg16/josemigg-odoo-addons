{
    "name": "Custom PDF Renderer (WeasyPrint)",
    "summary": "Reemplaza wkhtmltopdf con WeasyPrint para reportes PDF",
    "version": "17.0",
    "author": "josemig",
    "license": "LGPL-3",
    "category": "Tools",
    "depends": ["base", "account"],
    "assets": {
        "web.report_assets_basic": [
            "custom_pdf_renderer/static/src/css/basic_styles.min.css",
        ],
    },
    "data": [
        "views/ir_actions_report_views.xml",
    ],
    "external_dependencies": {
        "python": ["weasyprint"]
    },
    "installable": True,
    "auto_install": False,
    "application": False,
}
