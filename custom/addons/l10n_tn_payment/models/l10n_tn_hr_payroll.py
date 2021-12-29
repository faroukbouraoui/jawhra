# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import Warning, UserError
import odoo.addons.decimal_precision as dp
from datetime import datetime , timedelta, timezone, date


class hr_contract(models.Model):
    _inherit = 'hr.contract'

    nationalite = fields.Char('Nationalite', size=64)
    qualif = fields.Char('Qualification', size=64)
    niveau = fields.Char('Niveau', size=64)
    coef = fields.Char('Coefficient', size=64)
    base_nombre_jours = fields.Integer(' Base Nombre De Jours', size=64 )
    base_nombre_heure = fields.Float(' Base Nombre D\'heures', size=64 )
    base_tranche = fields.Integer(' Base Tranche', size=64 )
    # mode_pay = fields.Selection([('0', 'Versement'), ('1', 'Espéce')], string = 'Mode De Paiement', default=1)




class res_company(models.Model):
    _inherit = 'res.company'

    plafond_secu = fields.Float(string='Plafond de la Securite Sociale', digits=dp.get_precision('Payroll'))
    nombre_employes = fields.Integer(string='Nombre d\'employes')
    cotisation_prevoyance = fields.Float(string='Cotisation Patronale Prevoyance', digits=dp.get_precision('Payroll'))
    org_ss = fields.Char('Organisme de securite sociale', size=64)
    conv_coll = fields.Char('Convention collective', size=64)


class hr_payslip(models.Model):
    _inherit = 'hr.payslip'
    #
    # payment_mode = fields.Char('Mode de paiement',
    #                            # compute = 'get_payment', store = True ________oooooooooooooo___________________________________________________
    #                            )
    monthly = fields.Integer(string='mois en cours', compute='_get_annee', store=True)
    monthly_res = fields.Integer(string='Nombre de Paie restantes', compute='_get_annee', store=True)
    annee = fields.Integer(string="Annee en cours", compute='_get_annee', store=True)



    @api.depends('date_from')
    def _get_annee(self):

        for ps in self:
            d = datetime.strftime(ps.date_from, '%m')
            y = datetime.strftime(ps.date_from, '%Y')

            ps.annee = int(y)
            ps.monthly = int(d)
            ps.monthly_res= 12 - int(d)

    # @api.depends('struct_id')
    # def get_payment(self):
    #     for rec in self:
    #         xs = self.env['hr.contract'].search([('id', '=', self.contract_id.id)])
    #
    #         # rec.payment_mod = xs.mode_pay
    #         if xs.mod_pay =='0':
    #             print('espese')
    #         else:
    #             print('virement')







class hr_employee(models.Model):
    _inherit = 'hr.employee'

    matricule_cnss = fields.Char('Matricule CNSS', size=10)
    num_chezemployeur = fields.Integer('Numero chez l\'employeur')

    # @api.onchange('matricule_cnss')
    # def controle_saisie(self):
    #     while len(self.matricule_cnss) != 10:
    #         raise UserError("Le champ Matricule CNSS doit etre de 10 caracteres")
    #
    #
    # @api.onchange('passport_id')
    # def controle_saisie(self):
    #     while len(self.passport_id) != 10:
    #         raise UserError("Le champ Passeport doit etre de 10 caracteres")
    #
    # @api.onchange('identification_id')
    # def controle_saisie(self):
    #     while len(self.identification_id) != 10:
    #         raise UserError("Le champ CIN doit etre de 10 caracteres")




class hr_salary_rule(models.Model):
    _inherit = 'hr.salary.rule.category'

    remuneration = fields.Selection([('oui', 'oui'),('non','non')],default='oui')

    # @api.onchange('remuneration')
    # def onchange_remuneration(self):
    #
    #     if self.remuneration == 'oui'


