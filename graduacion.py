from odoo import models, fields, api
from odoo.exceptions import ValidationError

class GraduacionPaciente(models.Model):
    _name = 'optica.graduacion'
    _description = 'Graduación de Paciente'
    _rec_name = 'paciente_id'
    _order = 'fecha desc, id desc'  # opcional, útil en clínica

    paciente_id = fields.Many2one(
        'res.partner',
        string='Paciente',
        required=True,
        domain=[('is_company', '=', False)],
        ondelete='restrict',
        index=True,
    )
    fecha = fields.Date(string='Fecha de evaluación', default=fields.Date.context_today)
    profesional = fields.Many2one('res.users', string='Optometrista', default=lambda self: self.env.user)

    ojo_derecho_esfera = fields.Float(string='OD Esfera', digits=(8, 2))
    ojo_derecho_cilindro = fields.Float(string='OD Cilindro', digits=(8, 2))
    ojo_derecho_eje = fields.Integer(string='OD Eje')
    ojo_derecho_av = fields.Char(string='OD AV')

    ojo_izquierdo_esfera = fields.Float(string='OI Esfera', digits=(8, 2))
    ojo_izquierdo_cilindro = fields.Float(string='OI Cilindro', digits=(8, 2))
    ojo_izquierdo_eje = fields.Integer(string='OI Eje')
    ojo_izquierdo_av = fields.Char(string='OI AV')

    adicion = fields.Float(string='Adición', digits=(8, 2))
    distancia_nasopupilar_od = fields.Float(string='Distancia Nasopupilar OD', digits=(8, 2))
    distancia_nasopupilar_oi = fields.Float(string='Distancia Nasopupilar OI', digits=(8, 2))
    distancia_interpupilar = fields.Float(string='Distancia Interpupilar', digits=(8, 2))
    altura_centro_optico = fields.Float(string='Altura CO', digits=(8, 2))
    tipo_lente = fields.Selection([
        ('monofocal', 'Monofocal'),
        ('bifocal', 'Bifocal'),
        ('progresivo', 'Progresivo'),
    ], string='Tipo de Lente')

    diagnostico = fields.Selection([
        ('miopia', 'Miopía'),
        ('hipermetropia', 'Hipermetropía'),
        ('astigmatismo', 'Astigmatismo'),
        ('astigmatismo_miopico', 'Astigmatismo Miópico'),
        ('astigmatismo_hipermetropico', 'Astigmatismo Hipermetrópico'),
        ('astigmatismo_simple', 'Astigmatismo Simple'),
        ('presbicia', 'Presbicia'),
    ], string='Diagnóstico')

    observaciones = fields.Text(string='Observaciones')

    @api.constrains(
        'ojo_derecho_eje', 'ojo_izquierdo_eje',
        'ojo_derecho_esfera', 'ojo_izquierdo_esfera',
        'ojo_derecho_cilindro', 'ojo_izquierdo_cilindro'
    )
    def _check_valores(self):
        for rec in self:
            if rec.ojo_derecho_eje is not None and not (0 <= rec.ojo_derecho_eje <= 180):
                raise ValidationError('El eje del ojo derecho debe estar entre 0 y 180.')
            if rec.ojo_izquierdo_eje is not None and not (0 <= rec.ojo_izquierdo_eje <= 180):
                raise ValidationError('El eje del ojo izquierdo debe estar entre 0 y 180.')

            for campo, nombre in [
                (rec.ojo_derecho_esfera, 'OD Esfera'),
                (rec.ojo_izquierdo_esfera, 'OI Esfera'),
                (rec.ojo_derecho_cilindro, 'OD Cilindro'),
                (rec.ojo_izquierdo_cilindro, 'OI Cilindro'),
            ]:
                if campo is not None:
                    if not (-20.00 <= campo <= 20.00):
                        raise ValidationError(f'El valor de {nombre} debe estar entre -20.00 y +20.00.')
                    if abs((campo * 4) - round(campo * 4)) > 1e-8:
                        raise ValidationError(f'El valor de {nombre} debe ser múltiplo de 0.25 (p. ej., -1.25, 0.00, 2.50).')

    def action_imprimir_historia_clinica(self):
        """Imprime la historia clínica del paciente."""
        self.ensure_one()
        return self.env.ref('odoo_graduacion_paciente.action_report_graduacion_paciente').report_action(self)


class ResPartner(models.Model):
    _inherit = 'res.partner'
    graduacion_ids = fields.One2many('optica.graduacion', 'paciente_id', string='Graduaciones')
