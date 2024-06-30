from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ModelName(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread']
    _description = 'Hospital Patient'

    code = fields.Char(string="Sequence", readonly=True, required=True, default='/')
    name = fields.Char(string="Name and surname", copy=False)
    dni = fields.Char(string="DNI", copy=False, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('upgrade', 'Upgrade'),
        ('downgrade', 'Downgrade')], string="State", readonly=False, default='draft',
        required=True, index='btree', tracking=True)
    release_date = fields.Datetime(string="Release date", copy=False)
    update_date = fields.Datetime(string="Update date", copy=False)
    treatment_id = fields.Many2one('hospital.treatment', string="Treatment", copy=False)
    treatment_ids = fields.Many2many("hospital.treatment", "patient_treatment_rel" , string="Treatments",
                                    store=True,  copy=False)

    # ##################################################################
    # ########################### Button Methods #######################

    # ##################################################################
    # ########################### Onchange Methods #####################

    @api.onchange('dni')
    def _onchange_dni(self):
        self._check_dni()

    @api.onchange('treatment_id')
    def _compute_treatment(self):
        for patient in self.filtered(lambda p: p.treatment_id):
            if patient.treatment_id in patient.treatment_ids:
                continue
            patient.update({'treatment_ids': [(4, patient.treatment_id.id), None], 'treatment_id': False})

    # ###################################################################
    # ########################### Compute Methods #######################

    def _compute_display_name(self):
        for patient in self:
            patient.display_name = f"{patient.code != '/' and '%s - ' % patient.code or ''}{patient.name or _('No Name')}"

    # ###################################################################
    # ########################### Models Methods #######################

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', '/') == '/':
                vals['code'] = self.get_sequence()
        return super(ModelName, self).create(vals_list)

    # ###################################################################
    # ########################### Checks Methods ########################

    @api.constrains('dni')
    def _check_dni(self, to_check: str = ''):

        values, to_raise = to_check and [('', to_check)] or self.mapped(lambda p: (p.name, p.dni)), []
        for name, dni in values:
            if not dni: continue
            try:
                int(dni)
            except ValueError:
                to_raise.append(f"\n{name or _('No name')} - {dni}")

        if to_raise:
            raise UserError(_(f"Invalid DNI, Checks:\n{''.join(to_raise)}"))

        return True

    def _validate_sequence(self, raise_exception=True):
        sequence = self.env['ir.sequence'].search([('code', '=', 'vertical_hospital.patient')], )

        if not sequence and raise_exception:
            raise UserError(_(f'There is not a sequence for create the patient'))
        if len(sequence) > 1 and raise_exception:
            raise UserError(_(
                'There are multiple sequence for create patient. Review sequences with code vertical_hospital.patient'))
        return sequence

    # ###################################################################
    # ########################### Custom Methods ########################

    # ######## sequence management ########

    def get_sequence(self,raise_exception=True):
        sequence = self._validate_sequence(raise_exception)
        return sequence.next_by_id()


