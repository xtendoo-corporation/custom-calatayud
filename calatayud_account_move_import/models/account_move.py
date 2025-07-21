from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    imported_from_excel = fields.Boolean(
        string="Importado desde Excel",
        default=False,
        readonly=True,
        help="Indica si el asiento contable fue importado desde Excel"
    )

    excel_import_date = fields.Datetime(
        string="Fecha de importación",
        readonly=True,
        help="Fecha en la que se realizó la importación desde Excel"
    )

    @api.model
    def create_from_excel_data(self, move_data, lines_data):
        """
        Crea un asiento contable a partir de datos importados de Excel

        Args:
            move_data (dict): Datos del asiento contable
            lines_data (list): Lista de líneas del asiento contable

        Returns:
            account.move: Asiento contable creado
        """
        if not lines_data:
            raise UserError(_("No se encontraron líneas para importar."))

        # Comprobar el balance de las líneas
        total_debit = sum(line.get('debit', 0.0) for line in lines_data)
        total_credit = sum(line.get('credit', 0.0) for line in lines_data)

        if round(total_debit, 2) != round(total_credit, 2):
            raise UserError(_(
                "El asiento contable no está balanceado. "
                "Total Debe: {:.2f}, Total Haber: {:.2f}"
            ).format(total_debit, total_credit))

        # Crear el asiento
        move_vals = {
            'ref': move_data.get('ref', 'Importado desde Excel'),
            'date': move_data.get('date'),
            'journal_id': move_data.get('journal_id'),
            'move_type': 'entry',
            'imported_from_excel': True,
            'excel_import_date': fields.Datetime.now(),
            'line_ids': [(0, 0, line) for line in lines_data]
        }

        move = self.create(move_vals)
        return move
