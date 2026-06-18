{
    'name' : 'Hotel Management',
    'description' : "Hotel Management",
    'version' : '19.0.1.0.0',
    'application' : True,
    'category' : 'Hotel',
    'depends': ['base','mail','sale_management','contacts'],
    'data': [
        'data/ir_sequence_data.xml',
        'data/hotel_facility_data.xml',
        'data/hotel_food_category_data.xml',
        'data/hotel_room_data.xml',
        'data/hotel_food_items_data.xml',
        'data/hotel_product_data.xml',
        'data/hotel_email_template_checkout.xml',
        'data/email_corn.xml',
        'data/archive_corn.xml',
        'data/lunch_auto.xml',

        'security/hotel_management_groups.xml',
        'security/ir_rules.xml',
        'security/ir.model.access.csv',
        'report/ir_actions_report.xml',
        'report/ir_actions_report_templates.xml',

        'views/hotel_rooms_views.xml',
        'views/hotel_accommodation_views.xml',
        'views/hotel_food_category_views.xml',
        'views/hotel_order_list_views.xml',
        'views/hotel_order_food_views.xml',
        'views/hotel_food_items_views.xml',
        'views/hotel_facility_views.xml',
        'views/hotel_guest_views.xml',
        'views/hotel_payment_lines_views.xml',
        'wizard/hotel_food_items_wizard_views.xml',
        'wizard/hotel_management_report_wizard_views.xml',
        'views/hotel_menus.xml',
    ],
'assets':{
    'web.assets_backend':[
        'hotel_management/static/src/js/action_manager.js',]
}
}