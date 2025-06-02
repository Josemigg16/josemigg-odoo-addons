{
    "name": "Owl Components for Odoo",
    "summary": "Custom Owl components for Odoo",
    "version": "17.0",
    "author": "josemig",
    "license": "LGPL-3",
    "category": "Web",
    "depends": ["base", 'portal', 'web', 'website'],
    "assets": {
        'web.assets_frontend': [
            "custom_owl_components/static/src/components/**/*.js",
            "custom_owl_components/static/src/components/**/*.xml",
            "custom_owl_components/static/src/components/**/*.scss",
        ],
    },
    "data": [
        "views/example_page.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
}
