from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ModelName(models.Model):
    _name = 'hospital.treatment'
    _description = 'Hospital Treatment'

    code = fields.Char(string='Code', copy=False, required=True)
    name = fields.Char(string='Name',)
    doctor = fields.Char(string="Doctor")

    @api.constrains('code')
    def _check_code(self):
        """
           Ensure that the treatment code does not contain the sequence '026'.

           Raises
           ------
           UserError
               If any treatment code contains the sequence '026'.

        """
        to_checks = self.filtered(lambda treatment: treatment.code and '026' in treatment.code)
        if to_checks:
            raise UserError(_(
                f"The treatment code must not contain the sequence '026'. "
                f"Checks the next treatments:\n\n."
                f"{'-\n'.join(['%s: %s' % (t.name or _('No name'), t.code) for t in to_checks])}")
            )

