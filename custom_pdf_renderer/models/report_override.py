from odoo import models, _, fields
from odoo.exceptions import UserError
from collections import OrderedDict
from weasyprint import HTML
import io
import logging

_logger = logging.getLogger(__name__)

class ReportOverride(models.AbstractModel):
    _inherit = 'ir.actions.report'

    custom_engine = fields.Boolean(string="Custom Engine", default=False)

    def _render_qweb_pdf_prepare_streams(self, report_ref, data, res_ids=None):
        if not data:
            data = {}
        data.setdefault('report_type', 'pdf')

        report_sudo = self._get_report(report_ref)
        
        if not report_sudo.custom_engine:
            # Si no es el motor personalizado, llamamos al método original
            return super()._render_qweb_pdf_prepare_streams(report_ref, data, res_ids=res_ids)
        has_duplicated_ids = res_ids and len(res_ids) != len(set(res_ids))

        collected_streams = OrderedDict()

        if res_ids:
            records = self.env[report_sudo.model].browse(res_ids)
            for record in records:
                res_id = record.id
                if res_id in collected_streams:
                    continue
                collected_streams[res_id] = {
                    'stream': None,
                    'attachment': None,
                }

        res_ids_wo_stream = [res_id for res_id, stream_data in collected_streams.items() if not stream_data['stream']]

        # Si tenemos más de un registro, fallback a la implementación original
        if res_ids and len(res_ids) > 1:
            _logger.info("Multiple records detected, fallback to original wkhtmltopdf rendering for report %s", report_ref)
            return super()._render_qweb_pdf_prepare_streams(report_ref, data, res_ids=res_ids)

        # Caso con 0 o 1 registro: usar WeasyPrint
        all_res_ids_wo_stream = res_ids if has_duplicated_ids else res_ids_wo_stream

        if not res_ids or res_ids_wo_stream:
            # Renderizamos el HTML para esos registros
            html, _ = self._render_qweb_html(report_ref, all_res_ids_wo_stream, data=data)
            

            try:
                pdf_bytes = HTML(string=html).write_pdf()
            except Exception as e:
                raise UserError(_("Error generando PDF con WeasyPrint: %s") % e)

            pdf_content_stream = io.BytesIO(pdf_bytes)

            if has_duplicated_ids or not res_ids:
                return {
                    False: {
                        'stream': pdf_content_stream,
                        'attachment': None,
                    }
                }

            if len(res_ids_wo_stream) == 1:
                collected_streams[res_ids_wo_stream[0]]['stream'] = pdf_content_stream
                return collected_streams

        return collected_streams
