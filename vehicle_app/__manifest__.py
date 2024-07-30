{
    "name": "Vehicle Management",
    "author": "Aakash Pavar",
    "version": "1.0",
    "license": "LGPL-3",
    "depends": ["base", "account", "fleet", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/vehicle_service_history.xml",
        "views/vehicle_views.xml",
        "views/inherited_account_move_view.xml",
        "views/inherited_account_move_line_view.xml",
        "views/inherited_report_invoice.xml",
        "views/menu.xml",
    ],
    "application": True,
    "installable": True
}