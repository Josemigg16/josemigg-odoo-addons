from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
import json

import logging

_logger = logging.getLogger(__name__)

class ExampleController(http.Controller):

    @http.route('/example', type='http', auth='public', website=True, csrf=False)
    def example(self):
        users = request.env['res.users'].search([])
        values = {
            'users': users,
            'title': 'Example Owl Component',
        }
        return request.render('custom_owl_components.example_page_template', values)
    
    @http.route('/my/user-info', type='json', auth='user', website=True, csrf=False)  # auth='user' para que solo accedan usuarios logueados
    def user_info(self):
        user = request.env.user
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'employee_id': user.employee_id.id if user.employee_id else False,
        }
    
    @http.route('/update_employee', type='http', auth='public', csrf=False, methods=['POST'], website=True)
    def update_employee(self, **kwargs):
                
        employee_id = request.env.user.employee_id.id if request.env.user.employee_id else False

        if not employee_id:
            return request.make_response(
                json.dumps({'error': 'Missing employeeId'}),
                headers=[('Content-Type', 'application/json')]
            )
        
        try:
            employee_id = int(employee_id)
        except Exception:
            return request.make_response(
                json.dumps({'error': 'Invalid employeeId'}),
                headers=[('Content-Type', 'application/json')]
            )

        employee = request.env['hr.employee'].sudo().browse(employee_id)
        if not employee.exists():
            return request.make_response(
                json.dumps({'error': 'Employee not found'}),
                headers=[('Content-Type', 'application/json')]
            )
        
        employee.write({
            'name': kwargs.get('name', employee.name), 
            'country_of_birth': int(kwargs.get('country_of_birth') or employee.country_of_birth.id),
            })

        return request.make_response(
            json.dumps({'success': True, 'message': 'Employee updated successfully'}),
            headers=[('Content-Type', 'application/json')]
        )
