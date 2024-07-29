from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):

    _name = "hospital.patient"
    _description = 'Patient Records'
    _inherit = ['mail.thread']
    _sql_constraints = [
        ('check_date', 'CHECK(last_appointment<previous_appointment)',
         ' The Last date must be before the previous date !')
    ]

    name = fields.Char(string='Name ', required=True, tracking=True)
    address = fields.Char(string='Address ', tracking=True)
    age = fields.Integer(string='age', tracking=True)
    is_child = fields.Boolean(string='Is Child', tracking=True)
    notes = fields.Text(string='Notes')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others', 'Others')],
                              string='Gender', tracking=True)
    capitalized_name = fields.Char(string='Capitalized_Name ', compute='_compute_capitalized_name', store=True)
    ref = fields.Char(string="Reference", default=lambda self: _('New'))
    active = fields.Boolean(default=True)
    doctors_id = fields.Many2one('hospital.doctors', string="Doctor")
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')
    patient_image = fields.Image(string="Upload Patient Image")
    state = fields.Selection([('draft', 'Draft'),
                              ('progress', 'Progress'),
                              ('done', 'Done'),
                              ('paid', 'Paid')], string='State')
    id = fields.Integer(string='ID', required=True, readonly=True)
    last_appointment = fields.Datetime(string='The Last Appointment')
    previous_appointment = fields.Datetime(string='The previous Appointment')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    website = fields.Char(string='Website')
    appointment_count = fields.Integer(string='Appointment Count', compute='_appointment_count')

    @api.depends('appointment_ids')
    def _appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

    def print_patient_report(self):
        return self.env.ref("om_hospital.report_patient").report_action(self)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPaitient, self).create(vals_list)

    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 18:
            self.is_child = True
        else:
            self.is_child = False

    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_('You cannot delete a patient with appointments!'))

    @api.depends('name')
    def _compute_capitalized_name(self):
        for rec in self :
            if rec.name:
                rec.capitalized_name = rec.name.upper()
            else:
                rec.capitalized_name = ''

    @api.constrains('is_child', 'age')
    def _check_age_child(self):
        for rec in self:
            if rec.age == 0:
                raise ValidationError("Age has to be recorded")

    def action_test(self):
        print("Clicked")
        return

    def action_view_appointments(self):
        return {
            'name': _('Appointments'),
            'view_mode': 'tree,form',
            'res_model': 'hospital.appointment',
            'type': 'ir.actions.act_window',
            'context': {'default_patient_id': self.id},
            'target': 'current',
            'domain': [('patient_id', '=', self.id)],

        }


class ResPartner(models.Model):

    _inherit = 'res.partner'
