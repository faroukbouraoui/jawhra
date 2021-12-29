# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrderInheritance(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order Inheritance'

    # champ pour filtrer la vue de l'export
    is_export = fields.Boolean(string='Export')
    order_line_export = fields.One2many('sale.order.line', 'order_id', string='Order Lines',
                                        states={'cancel': [('readonly', True)], 'done': [('readonly', True)]},
                                        copy=True,
                                        auto_join=True)


class SaleOrderLineInheritance(models.Model):
    _inherit = 'sale.order.line'
    _description = 'Sale Order Line Inheritance'

    nb_carton = fields.Char(string='Nombre de carton')

    # poid brut = poid net * 1.06
    # poid net est la qtité en odoo standard

    poid_brut = fields.Float(string='Poid brut Unitaire', compute='_compute_poid_brut_', store=True)

    """
    partie export :
    consiste à calculer la quantité nette ==> meme formule de calcul en achat
    """

    product_uom_qty = fields.Float(string='Poid nette', digits='Product Unit of Measure', required=True, default=1.0,
                                   compute='_calcul_qte_nette_', inverse='_inverse_calcul_qte_nette_', store=True)
    caisse_id = fields.Many2one('caisse')
    qte_caisse = fields.Float(string='Qté caisse')
    qte_nette = fields.Float(string='Poid brut')
    poid_caisse = fields.Float(string='Poid Caisse', related='caisse_id.poid')

    @api.depends('product_uom_qty')
    def _compute_poid_brut_(self):
        for line in self:
            if line.product_uom_qty:
                line.poid_brut = line.product_uom_qty * 1.06

    @api.depends('qte_caisse', 'qte_nette', 'poid_caisse')
    def _calcul_qte_nette_(self):
        for line in self:
            if line.order_id.is_export is False:
                line.product_uom_qty = line.qte_nette - line.qte_caisse * line.poid_caisse

    def _inverse_calcul_qte_nette_(self):
        for line in self:
            if line.order_id.is_export is True:
                pass
