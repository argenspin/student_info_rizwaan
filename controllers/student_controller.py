from odoo import http
from odoo.http import request


class StudentList(http.Controller):
    @http.route(['/students'], type='http', auth="public", website=True, csrf=False)
    def student_list(self, **kw):
        students = request.env['student.details'].sudo().search([])
        return request.render("student_info_rizwaan.student_list_template",  {'students': students})