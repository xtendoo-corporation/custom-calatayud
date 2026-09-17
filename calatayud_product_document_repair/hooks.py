def post_init_hook(env):
    """Al instalar el módulo, repara los product.document que quedaron sin
    contenido (url vacía / fichero vacío) tras la migración de Odoo 17 a 18,
    recuperando el contenido desde su adjunto huérfano gemelo cuando se puede
    identificar sin ambigüedad."""
    env['product.document']._calatayud_repair_empty_documents()
