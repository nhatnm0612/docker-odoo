from odoo import api, SUPERUSER_ID

from . import controllers
from . import models


def pre_init_hook(cr):
    env = api.Environment(
        cr=cr,
        uid=SUPERUSER_ID,
        context={}
    )
    # region ::HIDE MENUES::
    website_menu = env.ref('website.menu_website_configuration')
    to_hide_menues = env['ir.ui.menu'].search(
        ['|', ('parent_id', '=', False), ('parent_id', '=', website_menu.id)]
    )
    to_hide_menues -= website_menu
    to_hide_menues -= env.ref('website_sale.menu_catalog')
    to_hide_menues -= env.ref('website.menu_dashboard')
    to_hide_menues.write({
        'groups_id': [(6, 0, [env.ref('base.group_no_one').id])]
    })
    # endregion

    # region ::SHOW PRODUCT VARIANTS::
    group_product_variant = env.ref('product.group_product_variant')
    group_product_variant.write({
        'users': [(4, env.ref('base.user_admin').id)]
    })
    # endregion

    # region ::INSTALL EN-VI LANGUAGE::
    langs = ['vi_VN', 'en_US']
    for lang in langs:
        rec = env['base.language.install'].create({
            'lang': lang, 'overwrite': True
        })
        rec.lang_install()

