{
    "name": "Óptica: Graduación de Paciente",
    "summary": "Historia clínica y graduaciones de pacientes",
    "version": "17.0.1.0.0",
    "author": "Christian Torres PeeWee",
    "website": "https://optica-zamora.com",
    "category": "Healthcare",
    "license": "LGPL-3",
    "depends": ["base", "web", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/graduaciones_view.xml",
        "report/report_historia_templates.xml",
        "report/report_historia_action.xml"
    ],
    "installable": True,
    "application": False
}
