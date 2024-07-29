{
    'name': 'Hospital Managment System','summary': "Manage a Hospital easily",
    'author': "Jihed Ha",
    'website': "https://www.facebook.com/profile.php?id=100079998342788",
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/menu.xml',
        'views/patient.xml',
        'views/doctors.xml',
        'views/appointment.xml',
        'views/cancel_days_views.xml',
        'reports/patient_template.xml',

    ],
'assets': {
        'web.assets_backend': [
            'om_hospital/static/src/css/custom_styles.css',
            'om_hospital/static/src/css/custom_button.css',
        ],
    },
    'depends': ['mail', 'base']
}
