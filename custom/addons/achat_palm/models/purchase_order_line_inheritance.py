# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AchatpalmPurchaseOrderLineInheritance(models.Model):
    _inherit = 'purchase.order.line'
    _description = 'Purchase Order Line Inheritance'

    product_qty = fields.Float(string='Poid net', digits='Product Unit of Measure', required=True,
                               compute='_calcul_qte_nette_', inverse='_inverse_calcul_qte_nette')
    caisse_id = fields.Many2one('caisse')
    qte_caisse = fields.Float(string='Qté caisse')
    qte_nette = fields.Float(string='Poid brut')
    poid_caisse = fields.Float(string='Poid Caisse', related='caisse_id.poid')

    # /!\ product_qty = "poid net", qte_nette = "poid brut"

    # /!\ ne se calcul pas immédiatement

    @api.depends('qte_caisse', 'qte_nette', 'poid_caisse')
    def _calcul_qte_nette_(self):
        for line in self:
            line.product_qty = line.qte_nette - line.qte_caisse * line.poid_caisse

    def _inverse_calcul_qte_nette(self):
        for line in self:
            if line.qte_nette:
                pass
