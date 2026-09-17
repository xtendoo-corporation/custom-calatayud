import logging

from odoo import _, models

_logger = logging.getLogger(__name__)


class ProductDocument(models.Model):
    _inherit = 'product.document'

    def _calatayud_find_empty(self):
        """Return the product.document recordset whose underlying attachment
        has no actual content (empty url for links, no file for binaries)."""
        docs = self.sudo().search([])
        return docs.filtered(
            lambda d: (d.type == 'url' and not d.url)
            or (d.type == 'binary' and not d.store_fname and not d.db_datas)
        )

    def _calatayud_find_twin(self, doc):
        """Find the orphaned ir.attachment "twin" of `doc`: same name, same
        exact create_date, same type, not linked to any record, and holding
        real content. Returns a recordset (empty, one, or several matches)."""
        Attachment = self.env['ir.attachment'].sudo()
        domain = [
            ('id', '!=', doc.ir_attachment_id.id),
            ('name', '=', doc.name),
            ('create_date', '=', doc.create_date),
            ('type', '=', doc.type),
            ('res_model', '=', False),
        ]
        candidates = Attachment.search(domain)
        if doc.type == 'url':
            candidates = candidates.filtered(lambda a: a.url)
        else:
            candidates = candidates.filtered(lambda a: a.store_fname or a.db_datas)
        return candidates

    def _calatayud_repair_empty_documents(self):
        """Repair product.document records left content-less by the Odoo 17 ->
        18 migration, recovering the content from their orphaned twin
        ir.attachment when it can be identified without ambiguity.

        Returns a dict with the documents repaired and the ones left for
        manual review (no twin found, or more than one candidate twin).
        """
        empty_docs = self._calatayud_find_empty()
        repaired = []
        unresolved = []

        for doc in empty_docs:
            twin = self._calatayud_find_twin(doc)
            if len(twin) == 1:
                if doc.type == 'url':
                    doc.ir_attachment_id.write({'url': twin.url})
                else:
                    doc.ir_attachment_id.write({
                        'mimetype': twin.mimetype,
                        'raw': twin.raw,
                    })
                repaired.append((doc.id, doc.name))
            else:
                unresolved.append((doc.id, doc.name, doc.res_id, len(twin)))

        _logger.info(
            "calatayud_product_document_repair: %s documento(s) reparado(s), "
            "%s sin resolver automáticamente", len(repaired), len(unresolved)
        )
        if unresolved:
            _logger.warning(
                "calatayud_product_document_repair: documentos sin resolver "
                "(id documento, nombre, res_id producto, nº candidatos): %s",
                unresolved,
            )

        print("\n" + "=" * 80)
        print("REPARACIÓN DE DOCUMENTOS DE PRODUCTO - CALATAYUD")
        print(f"Reparados automáticamente: {len(repaired)}")
        print(f"Pendientes de revisión manual: {len(unresolved)}")
        for doc_id, name, res_id, n_candidates in unresolved:
            print(f"  - documento {doc_id} ({name!r}) producto {res_id}: {n_candidates} candidato(s)")
        print("=" * 80 + "\n")

        return {'repaired': repaired, 'unresolved': unresolved}

    def action_calatayud_repair_empty_documents(self):
        """Acción manual para relanzar la reparación (por ejemplo, si se crean
        más documentos vacíos después de instalar el módulo)."""
        result = self._calatayud_repair_empty_documents()
        message = _(
            "Documentos reparados: %(repaired)s. Pendientes de revisión manual: %(unresolved)s.",
            repaired=len(result['repaired']),
            unresolved=len(result['unresolved']),
        )
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Reparación de documentos"),
                'message': message,
                'sticky': True,
            },
        }
