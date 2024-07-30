{
    "name": "Real Estate Management",
    "author": "Aakash Pavar",
    "version": "17.0.1.1",
    "license": "LGPL-3",
    "category": "Property Business",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_type_view.xml",
        "views/estate_property_views.xml",
        "views/estate_property_tag_view.xml",
        "views/res_users_view.xml",
        "views/estate_menus.xml",
        ],
    'assets': {
        'web.assets_backend': [
            'real_estate/static/src/css/custom_button.css',
        ],
    },
    'installable': True,
    'application': True,
}