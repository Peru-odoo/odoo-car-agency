from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalDoctors(models.Model):

    _name = "hospital.doctors"
    _description = 'Doctors Records'
    _inherit = 'mail.thread'
    # _inherits = {'hospital.patient': 'tag_ids'}
    _rec_name = 'ref'
    _sql_constraints = [
        ('check_name_and_age', 'CHECK(age != 40 )', 'age and name must be different !'),
        ('unique_name', 'UNIQUE(name)', 'The name must be unique !'),
        ('unique_id', 'UNIQUE(lid)', 'The ID must be unique ! ')
    ]

    name = fields.Char(string='name ', required=True, tracking=True)
    lid = fields.Char(string='ID', tracking=True)
    age = fields.Integer(string='age', tracking=True)
    notes = fields.Text(string='Notes')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others', 'Others')],
                              string='Gender', tracking=True)
    ref = fields.Char(string="Reference", default=lambda self: _('New'))
    active = fields.Boolean(default=True)
    patient_ids = fields.One2many('hospital.patient', 'doctors_id', string='Patients')
    tag_ids = fields.Many2many('res.partner.category', 'hospital_doctors_tag', 'patient_id', 'tag_id'
                               , string='Tags')

    def name_get(self):
        res = []
        for rec in self :
            res.append((rec.id, f'{rec.ref}-{rec.name}'))
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.doctors')
        return super(HospitalDoctors, self).create(vals_list)

    @api.constrains('is_child', 'age')
    def _check_age_child(self):
        for rec in self:
            if rec.age < 23:
                raise ValidationError(_("Age has to be real "))
