# -*- coding: utf-8 -*-
from odoo import http

# class TimeSheetModule(http.Controller):
#     @http.route('/time_sheet_module/time_sheet_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/time_sheet_module/time_sheet_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('time_sheet_module.listing', {
#             'root': '/time_sheet_module/time_sheet_module',
#             'objects': http.request.env['time_sheet_module.time_sheet_module'].search([]),
#         })

#     @http.route('/time_sheet_module/time_sheet_module/objects/<model("time_sheet_module.time_sheet_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('time_sheet_module.object', {
#             'object': obj
#         })