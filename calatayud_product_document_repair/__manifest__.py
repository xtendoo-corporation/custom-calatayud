{
    'name': 'Calatayud Product Document Repair',
    'version': '18.0.1.0.0',
    'category': 'Website/Website',
    'summary': 'Recupera el contenido perdido de los documentos de producto tras la migración 17 a 18',
    'description': """
        Módulo de corrección de datos (Odoo 17 -> 18): documentos de producto vacíos.

        Diagnóstico:
        Cada "Documento" de producto (product.document, visible en la pestaña
        Comercio electrónico y en la web como "Documentos") delega en un
        ir.attachment (_inherits). Se detectó que para un gran número de estos
        documentos, el ir.attachment vinculado al producto quedó SIN contenido
        (url vacía en los de tipo enlace, o sin fichero en los de tipo binario),
        mientras que existe OTRO ir.attachment "huérfano" (sin res_model/res_id),
        con el mismo nombre y la MISMA fecha de creación exacta (al microsegundo),
        que sí contiene el contenido real. Todo indica que en algún proceso de
        importación/migración se crearon dos adjuntos en la misma operación y solo
        uno de los dos conservó el contenido.

        Corrección:
        Al instalar el módulo (post_init_hook), por cada product.document vacío se
        busca su pareja huérfana por (nombre, fecha de creación exacta). Si hay una
        única coincidencia con contenido real, se copia al documento del producto.
        Si no hay coincidencia única (0 o más de 1), el documento se deja intacto y
        se reporta en el log del servidor para revisión manual.

        También se expone la acción `action_calatayud_repair_empty_documents` en
        `product.document` para poder relanzar la reparación manualmente (por si se
        crean más documentos vacíos después de instalar el módulo).
    """,
    'author': 'Guillermo Barcena Lopez',
    'depends': [
        'base',
        'product',
        'website_sale',
    ],
    'data': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'post_init_hook': 'post_init_hook',
}
