# -*- coding: utf-8 -*-
# from odoo import http


# class ReportPalm(http.Controller):
#     @http.route('/report_palm/report_palm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_palm/report_palm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_palm.listing', {
#             'root': '/report_palm/report_palm',
#             'objects': http.request.env['report_palm.report_palm'].search([]),
#         })

#     @http.route('/report_palm/report_palm/objects/<model("report_palm.report_palm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_palm.object', {
#             'object': obj
#         })
