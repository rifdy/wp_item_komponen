# -*- coding: utf-8 -*-
{
    'name': "Warung Pintar : Item Komponen",

    'summary': """
        Warung Pintar
    """,

    'description': """
        Modul Baru untuk Item dan Komponen
    """,

    'author': "Rifdy Fachry",

    'version': '1.0',

    'depends': ['base'],

    'data': [
        'views/wr_item.xml',
        'views/wr_component.xml',
        'views/templates.xml',
        'wizard/wr_item_import.xml'
    ],
    'qweb': [
        "static/src/xml/wr_custom_import_item.xml",
    ],
 
}