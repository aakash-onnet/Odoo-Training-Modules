# noinspection PyStatementEffect
{
    "name": "Hospital Management System",
    "author": "Aakash Pavar",
    "version": "17.0.1.1",
    "license": "LGPL-3",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/patient_readonly_view.xml",
        "views/patient_view.xml",
        "views/female_patient.xml",
        "views/doctor_view.xml",
        "views/menu.xml",
    ],
    'installable': True,
    'application': True,
}
