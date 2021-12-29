# -*- coding: utf-8 -*-
# from odoo import http


# class ReportCompany(http.Controller):
#     @http.route('/report_company/report_company/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_company/report_company/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_company.listing', {
#             'root': '/report_company/report_company',
#             'objects': http.request.env['report_company.report_company'].search([]),
#         })

#     @http.route('/report_company/report_company/objects/<model("report_company.report_company"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_company.object', {
#             'object': obj
#         })
