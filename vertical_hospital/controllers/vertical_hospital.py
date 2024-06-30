from odoo import http
from odoo.http import request, Response
from odoo.tools import json


class VerticalHospital(http.Controller):

    @http.route('/pacientes/consulta/<string:sequence>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_patients(self, sequence):
        if not request.env['ir.config_parameter'].sudo().get_param('vertical_hospital.endpoint'):
            return Response(
                json.dumps({'results': {'code': 503, 'message': "<p>Service disabled.Contact you administrator</p>"}})
            )
        p = request.env['hospital.patient'].sudo().search([('code', '=', sequence)], limit=1)
        response = p and {'seq': p.code, 'name': p.name, 'dni': p.dni , 'state': p.state} or {}
        headers = {'Content-Type': 'application/json'}

        return Response(json.dumps(response), headers=headers)
