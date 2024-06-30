from odoo import http
from odoo.http import request, Response
from odoo.tools import json


class VerticalHospital(http.Controller):

    @http.route('/pacientes/consulta/<string:sequence>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_patients(self, sequence):
        """
        Retrieve patient information based on a unique sequence code.

        Parameters
        ----------
        sequence : str
            The unique sequence code of the patient to search for.

        Returns
        -------
        Response
            A JSON response containing patient information if found, otherwise an
            appropriate message indicating the service status or that the patient
            was not found.

        Notes
        -----
        - The method checks if the endpoint is enabled via a configuration parameter.
        - The response is formatted as JSON with appropriate headers.
        - If the patient is not found, an empty dictionary is returned.
        """
        if not request.env['ir.config_parameter'].sudo().get_param('vertical_hospital.endpoint'):
            return Response(
                json.dumps({'results': {'code': 503, 'message': "<p>Service disabled.Contact you administrator</p>"}})
            )
        p = request.env['hospital.patient'].sudo().search([('code', '=', sequence)], limit=1)
        response = p and {'seq': p.code, 'name': p.name, 'dni': p.dni , 'state': p.state} or {}
        headers = {'Content-Type': 'application/json'}

        return Response(json.dumps(response), headers=headers)
