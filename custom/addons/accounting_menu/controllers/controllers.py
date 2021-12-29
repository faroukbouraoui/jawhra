# -*- coding: utf-8 -*-
# from odoo import http


# class AccountingMenu(http.Controller):
#     @http.route('/accounting_menu/accounting_menu/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/accounting_menu/accounting_menu/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('accounting_menu.listing', {
#             'root': '/accounting_menu/accounting_menu',
#             'objects': http.request.env['accounting_menu.accounting_menu'].search([]),
#         })

#     @http.route('/accounting_menu/accounting_menu/objects/<model("accounting_menu.accounting_menu"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('accounting_menu.object', {
#             'object': obj
#         })
