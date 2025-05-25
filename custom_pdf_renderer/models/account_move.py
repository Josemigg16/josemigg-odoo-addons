from odoo import models
import base64
import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def get_partner_image_base64(self):
        """Retorna la imagen del partner en base64 para usar en weasyprint."""
        _logger.info("Entrando a get_partner_image_base64() para %s", self.name)
        self.ensure_one()
        if self.partner_id and self.partner_id.image_1920:
             return 'data:image/png;base64,%s' % self.partner_id.image_1920
        return False
