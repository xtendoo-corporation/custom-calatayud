{
    "name": "Document format Calatayud",
    "version": "16.0",
    "author": "Salvador Gonzalez (https://xtendoo.es)",
    "category": "Calatayud",
    "license": "AGPL-3",
    'depends': [
        'base_setup',
        'product',
        'analytic',
        'account_payment_partner',
        'portal',
        'purchase',
        'sale',
        'base',
        'stock',
        'stock_picking_report_valued',
    ],
    "data": [
        "views/report_picking.xml",
        "views/invoice_document.xml",
        "views/sale_order_document.xml",
        "views/report_deliveryslip.xml",
        "views/purchase_order_document.xml",
        "views/report_payment_receipt_templates.xml",
    ],
    "installable": True,
    "auto_install": False,
}
