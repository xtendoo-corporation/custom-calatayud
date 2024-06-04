{
    "name": "Document format Calatayud",
    "version": "16.0",
    "author": "Salvador Gonzalez (https://xtendoo.es)",
    "category": "Calatayud",
    "license": "AGPL-3",
    'depends': ['base_setup', 'product', 'analytic', 'portal', 'digest', 'sale', 'base', 'stock', 'stock_picking_report_valued'],
    "data": [
        "views/invoice_document.xml",
        "views/sale_order_document.xml",
        "views/report_deliveryslip.xml",
        "views/report_purchaseorder_document_calatayud.xml",
    ],
    "installable": True,
    "auto_install": False,
}
