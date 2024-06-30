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
    treatment_ids = fields.Many2many("hospital.treatment", "patient_treatment_rel", string="Treatments",
                                    store=True,  copy=False)

    # ##################################################################
    # ########################### Onchange Methods #####################

    @api.onchange('dni')
    def _onchange_dni(self):
        """
        Triggered when the DNI field is changed. Checks the validity of the DNI.
        """
        self._check_dni()

    @api.onchange('treatment_id')
    def _compute_treatment(self):
        """
        Updates the patient's treatments when a new treatment is selected.

        Notes
        -----
        This method is called automatically by Odoo when the treatment_id field is modified.
        """
        for patient in self.filtered(lambda p: p.treatment_id):
            if patient.treatment_id in patient.treatment_ids:
                continue
            patient.update({'treatment_ids': [(4, patient.treatment_id.id), None], 'treatment_id': False})

    # ###################################################################
    # ########################### Compute Methods #######################

    def _compute_display_name(self):
        """
        Computes the display name of the patient.
        """
        for patient in self:
            patient.display_name = f"{patient.code != '/' and '%s - ' % patient.code or ''}{patient.name or _('No Name')}"

    # ###################################################################
    # ########################### Models Methods #######################

    @api.model_create_multi
    def create(self, vals_list):
        """
        Create multiple patient records. Ensures each patient has a unique sequence code.

        Parameters
        ----------
        vals_list : list of dict
            List of dictionaries with patient data.

        Returns
        -------
        recordset
            Newly created patient records.

        """
        for vals in vals_list:
            if vals.get('code', '/') == '/':
                vals['code'] = self.get_sequence()
        return super(ModelName, self).create(vals_list)

    # ###################################################################
    # ########################### Checks Methods ########################

    @api.constrains('dni')
    def _check_dni(self, to_check: str = ''):
        """
        Ensure the DNI is valid.

        Parameters
        ----------
        to_check : str, optional
            Specific DNI to check (default is '').

        Raises
        ------
        UserError
            If any DNI is invalid.

        Returns
        -------
        bool
            True if all DNIs are valid.
        """
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
        """
        Validate the patient sequence.

        Parameters
        ----------
        raise_exception : bool, optional
            Whether to raise an exception if validation fails (default is True).

        Raises
        ------
        UserError
            If there is no sequence or multiple sequences found for creating patients.

        Returns
        -------
        recordset
            The sequence record.

        """
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

    def get_sequence(self, raise_exception=True):
        """
        Get the next value in the patient sequence.

        Parameters
        ----------
        raise_exception : bool, optional
            Whether to raise an exception if validation fails (default is True).

        Returns
        -------
        str
            The next sequence value.

        """
        sequence = self._validate_sequence(raise_exception)
        return sequence.next_by_id()
