# -*- coding: utf-8 -*-

from odoo import models, fields, api


class res_company(models.Model):
    _inherit = 'res.company'
    _description = 'change string field in res_company'

    # ajout champ vat
    mf = fields.Char('Matricule fiscal')

