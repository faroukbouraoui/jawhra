# -*- coding: utf-8 -*-

from odoo import models, fields


class Caisse(models.Model):
    _name = 'caisse'
    _rec_name = 'nom'
    """
     une table "caisse" qui contient des enregistrements par défeaut
     """

    nom = fields.Char()
    poid = fields.Float()
