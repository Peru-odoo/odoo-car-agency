import logging
from odoo import api, fields, models, _


_logger = logging.getLogger(__name__)


class HospitalAppointment(models.Model):

    _name = "hospital.appointment"
    _description = 'Patients appointments '
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id"

    ref = fields.Char(string='Order Reference', required=True, tracking=True)
    doctors_id = fields.Many2one('hospital.doctors', string="Doctor")
    patient_id = fields.Many2one('hospital.patient', string="patient")
    date = fields.Datetime(string='Date')
    description = fields.Selection([('deserves_treatment', 'Deserves Treatment'),
                                   ('recovered', 'Recovered')], string='description')
    state = fields.Selection([('cancel', 'Cancel'), ('draft', 'Draft'), ('in_consultations', 'In Consultations'),
                              ('confirmed', 'Confirmed'), ('done', 'Done')], string='Status')
    id = fields.Char(string="Reference", default=lambda self: _('New'))
    sequence = fields.Integer(string="Sequence", default=1)
    active = fields.Boolean(default=True)
    notes = fields.Text(string='Notes')
    progress = fields.Integer(string='Progress', compute='_compute_progress')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")

    api.depends('state')

    def _compute_progress(self):
        for rec in self:
            try:
                if rec.state == 'draft':
                    rec.progress = 25
                elif rec.state == 'cancel':
                    rec.progress = 0
                elif rec.state == 'done':
                    rec.progress = 75
                elif rec.state == 'in_consultations':
                    rec.progress = 50
                elif rec.state == 'confirmed':
                    rec.progress = 100
                else:
                    rec.progress = 0  # Assign a default value if state is somehow not set or unknown

                # Log the computed progress for debugging purposes
                _logger.info(f"Computed progress for appointment {rec.id}: {rec.progress}")

            except Exception as e:
                _logger.error(f"Failed to compute progress for record {rec.id}: {e}")
                rec.progress = 0  # Assign a default value in case of an error
