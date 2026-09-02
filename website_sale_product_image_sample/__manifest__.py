
{
    "name": "Website sale product image sample",
    "summary": """Display product image sample to select product variant on website""",
    "version": "18.0.1.0.0",
    "development_status": "Production/Stable",
    "website": "https://github.com/OCA/e-commerce",
    "author": "Xtendoo, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "category": "eCommerce",
    "installable": True,
    "auto_install": False,
    "application": False,
    "depends": [
        "sale",
        "website_sale",
        # Ensure POS is loaded before our point_of_sale assets and that
        # imports like @point_of_sale/... resolve correctly in the client.
        "point_of_sale",
    ],
    "data": [
        "views/variants.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_sale_product_image_sample/static/src/css/product_configurator.scss",
        ],
        'web.assets_backend': [
            'website_sale_product_image_sample/static/src/xml/product_attribute_image.xml',
            'website_sale_product_image_sample/static/src/js/product_attribute_image.js',
        ],
        'point_of_sale._assets_pos': [
            'website_sale_product_image_sample/static/src/css/pos_product_attribute_image.scss',
            'website_sale_product_image_sample/static/src/js/pos_product_attribute_image.js',
            'website_sale_product_image_sample/static/src/xml/pos_product_attribute_image.xml',
        ],
    },
}
