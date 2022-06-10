{
    'name': 'Handy Craft Village',
    'version': '15.0.0.1.0',
    'description': '',
    'summary': 'For showing the world who we are',
    'author': 'nhatnguyenminh061289@gmail.com',
    'website': 'https://github.com/nhatnm0612',
    'license': 'LGPL-3',
    'category': '',
    'depends': [
        'website_sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/website_menu_data.xml',
        'data/website_rewrite_data.xml',
        'views/website_post_views.xml',
        'views/menuitems.xml',
        'views/templates.xml',
    ],
    'pre_init_hook': 'pre_init_hook',
    'auto_install': False,
    'application': True,
    'assets': {
        'web.assets_frontend': [
            'handy_craft_village/static/src/css/website.css',
        ]
    },
}
