import base64
import tempfile
import logging
import os
from datetime import datetime
from io import BytesIO

import xlrd
from odoo import fields, models, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class ImportAccountMove(models.TransientModel):
    _name = 'import.account.move'
    _description = 'Importador de Asientos Contables desde Excel'

    journal_id = fields.Many2one(
        'account.journal',
        string='Diario',
        required=True,
        domain=[('type', '=', 'general')],
        help='Diario en el que se creará el asiento contable'
    )

    date = fields.Date(
        string='Fecha del asiento',
        required=True,
        default=fields.Date.context_today,
        help='Fecha en la que se registrará el asiento contable'
    )

    file = fields.Binary(
        string='Archivo Excel',
        help='Archivo Excel con los datos del asiento contable'
    )

    filename = fields.Char(
        string='Nombre del archivo'
    )

    state = fields.Selection(
        [('import', 'Importar'), ('result', 'Resultado')],
        default='import',
        string='Estado'
    )

    move_id = fields.Many2one(
        'account.move',
        string='Asiento contable creado',
        readonly=True
    )

    # Archivo por defecto incluido en el módulo
    use_default_file = fields.Boolean(
        string='Usar archivo por defecto',
        default=False,
        help='Si está marcado, se usará el archivo ASIENTO CIERRE 2024.xlsx incluido en el módulo'
    )

    @api.model
    def _get_default_file_path(self):
        module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(module_path, 'data', 'ASIENTO CIERRE 2024.xlsx')

    def action_import(self):
        """Acción para importar asientos contables desde Excel"""
        self.ensure_one()

        # Determinar si usamos el archivo por defecto o el subido por el usuario
        if self.use_default_file:
            file_path = self._get_default_file_path()
            if not os.path.exists(file_path):
                raise UserError(_("No se encontró el archivo por defecto en %s") % file_path)

            with open(file_path, 'rb') as f:
                file_content = f.read()
        else:
            if not self.file:
                raise UserError(_("Por favor, seleccione un archivo Excel para importar."))
            file_content = base64.b64decode(self.file)

        # Procesar el archivo Excel
        try:
            move_data, lines_data = self._process_excel_file(file_content)
        except Exception as e:
            _logger.error("Error procesando el archivo Excel: %s", str(e))
            raise UserError(_("Error procesando el archivo Excel: %s") % str(e))

        # Crear el asiento contable
        move_data.update({
            'journal_id': self.journal_id.id,
            'date': self.date,
        })

        try:
            move = self.env['account.move'].create_from_excel_data(move_data, lines_data)
            self.write({
                'state': 'result',
                'move_id': move.id,
            })
        except Exception as e:
            _logger.error("Error creando el asiento contable: %s", str(e))
            raise UserError(_("Error creando el asiento contable: %s") % str(e))

        return {
            'name': _('Importador de Asientos Contables'),
            'type': 'ir.actions.act_window',
            'res_model': 'import.account.move',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def action_view_move(self):
        """Ver el asiento contable creado"""
        self.ensure_one()
        if not self.move_id:
            raise UserError(_("No hay ningún asiento contable creado."))

        return {
            'name': _('Asiento Contable Importado'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.move_id.id,
            'target': 'current',
        }

    def _process_excel_file(self, file_content):
        """
        Procesa el archivo Excel y extrae los datos para crear el asiento contable

        Args:
            file_content (bytes): Contenido del archivo Excel

        Returns:
            tuple: (move_data, lines_data)
                - move_data (dict): Datos del asiento contable
                - lines_data (list): Lista de líneas del asiento contable
        """
        # Crear un archivo temporal para el Excel
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name

        try:
            # Abrir el archivo Excel
            workbook = xlrd.open_workbook(temp_file_path)
            worksheet = workbook.sheet_by_index(0)

            # Inicializar datos del movimiento
            move_data = {'ref': 'Asiento importado de Excel: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

            # Leer la fecha del asiento de la fila 0 (primera fila del Excel)
            if worksheet.nrows > 0:
                try:
                    # Intentar obtener la fecha de la celda A1 (fila 0, columna 0)
                    cell_value = worksheet.cell_value(0, 0)
                    if isinstance(cell_value, float):
                        # Si es un número float, intentar convertirlo a fecha de Excel
                        try:
                            date_tuple = xlrd.xldate_as_tuple(cell_value, workbook.datemode)
                            move_date = datetime(date_tuple[0], date_tuple[1], date_tuple[2]).date()
                            move_data['date'] = move_date
                            _logger.info(f"Se utilizará la fecha {move_date} del Excel para el asiento contable")
                        except Exception as e:
                            _logger.warning(f"No se pudo convertir el valor '{cell_value}' a fecha: {str(e)}")
                    elif isinstance(cell_value, str) and cell_value:
                        # Si es una cadena, intentar varios formatos de fecha
                        for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d', '%Y-%m-%d']:
                            try:
                                move_date = datetime.strptime(cell_value, fmt).date()
                                move_data['date'] = move_date
                                _logger.info(f"Se utilizará la fecha {move_date} del Excel para el asiento contable")
                                break
                            except ValueError:
                                continue
                except Exception as e:
                    _logger.warning(f"Error al leer la fecha de la primera fila: {str(e)}")

            # Extraer datos de las líneas
            lines_data = []
            errors = []  # Lista para recopilar errores

            # Empezar desde la fila 1 (saltando la fila de fecha)
            for row_index in range(1, worksheet.nrows):
                row = worksheet.row(row_index)

                # Verificar si la fila tiene datos
                if not any(cell.value for cell in row):
                    continue

                # Obtener los valores de las columnas
                try:
                    # Verificar que las columnas A, B y E (columnas 0, 1 y 4) estén rellenas
                    if not row[0].value or not row[1].value or not row[3].value or not row[4].value:
                        continue

                    # O = columna 14 (debe), R = columna 17 (haber), E = columna 4 (código cuenta/subcuenta), I = columna 8 (descripción)
                    debit = float(row[14].value) if len(row) > 14 and row[14].value else 0.0  # Columna O - debe
                    credit = float(row[17].value) if len(row) > 17 and row[17].value else 0.0  # Columna R - haber
                    name = str(row[8].value).strip() if len(row) > 8 and row[8].value else 'Línea importada'  # Columna I - descripción

                    # Obtener la subcuenta/código de cuenta de la columna E (índice 4)
                    # Esta columna contiene tanto el código de cuenta como la subcuenta
                    if len(row) > 4 and row[4].value:
                        if isinstance(row[4].value, float):
                            if row[4].value == int(row[4].value):
                                account_code = str(int(row[4].value))
                            else:
                                account_code = str(row[4].value)
                        else:
                            account_code = str(row[4].value).strip()
                    else:
                        continue  # Si no hay código de cuenta, saltar esta fila

                    # La subcuenta es la misma que el código de cuenta (columna E)
                    subcuenta = account_code

                    # Obtener la referencia del partner de la columna G (índice 6)
                    partner_ref = str(row[6].value).strip() if len(row) > 6 and row[6].value else ""  # Columna G - referencia partner

                    if not account_code:
                        continue

                    # Buscar la cuenta por código
                    account = self.env['account.account'].search([('code', '=', account_code)], limit=1)
                    if not account:
                        errors.append(_("Fila %s: No se encontró la cuenta con código: %s") % (row_index + 1, account_code))
                        continue

                    # Verificar si la subcuenta requiere partner (subcuentas que empiecen por 400, 410 o 430)
                    partner_id = False
                    requires_partner = self._account_requires_partner(subcuenta)

                    if requires_partner:
                        if not partner_ref:
                            errors.append(_("Fila %s: La subcuenta %s requiere un partner. Debe proporcionar una referencia en la columna G.") % (row_index + 1, subcuenta))
                            continue

                        # Buscar el partner por el campo 'ref'
                        partner = self.env['res.partner'].search([('ref', '=', partner_ref)], limit=1)
                        if not partner:
                            errors.append(_("Fila %s: No se encontró un partner con la referencia '%s' para la subcuenta %s.") % (row_index + 1, partner_ref, subcuenta))
                            continue

                        partner_id = partner.id
                        _logger.info(f"Partner encontrado: {partner.name} (ref: {partner_ref}) para la subcuenta {subcuenta}")
                    elif partner_ref:
                        # Si hay referencia de partner pero no es obligatorio, intentar buscarlo igual
                        partner = self.env['res.partner'].search([('ref', '=', partner_ref)], limit=1)
                        if partner:
                            partner_id = partner.id
                            _logger.info(f"Partner opcional encontrado: {partner.name} (ref: {partner_ref}) para la subcuenta {subcuenta}")
                        else:
                            _logger.warning(f"Partner con referencia '{partner_ref}' no encontrado, pero no es obligatorio para la subcuenta {subcuenta}")

                    line_data = {
                        'account_id': account.id,
                        'name': name,
                        'debit': debit,
                        'credit': credit,
                        'partner_id': partner_id,
                    }

                    # Buscar analíticas si están disponibles en otras columnas
                    # (evitamos la columna E que ahora es subcuenta)

                    lines_data.append(line_data)

                except Exception as e:
                    errors.append(_("Fila %s: Error procesando la fila: %s") % (row_index + 1, str(e)))
                    continue

            # Verificar si hay errores antes de continuar
            if errors:
                error_summary = _("Se encontraron los siguientes errores:\n\n") + "\n".join(errors)
                raise UserError(error_summary)

            if not lines_data:
                raise UserError(_("No se encontraron líneas válidas en el archivo."))

            return move_data, lines_data

        except xlrd.XLRDError as e:
            raise UserError(_("Error leyendo el archivo Excel: %s") % str(e))
        finally:
            # Eliminar el archivo temporal
            try:
                os.unlink(temp_file_path)
            except:
                pass

    def _account_requires_partner(self, account_code):
        """
        Verifica si una cuenta requiere partner obligatorio

        Args:
            account_code (str): Código de la cuenta contable

        Returns:
            bool: True si la cuenta requiere partner, False en caso contrario
        """
        return account_code.startswith(('400', '410', '430'))
