# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, exceptions
from datetime import date, datetime, timedelta
from stdnum.exceptions import ValidationError


def get_years():
    year_list = []

    for i in range(2021, 2070):
        year_list.append((str(i), str(i)))
    return year_list


class TimeSheet(models.Model):
    _name = 'time_sheet_module.time'
    _description = 'Time Sheet'

    @api.model
    def default_get(self, fields):
        res = super(TimeSheet, self).default_get(fields)
        modele_lines = []
        employee_rec = self.env['hr.employee'].search([('active', '=', True)])
        for emp in employee_rec:
            line = (0, 0, {
                'employee_id': emp.id,
            }, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0,

                    )
            modele_lines.append(line)
        res.update({
            'model_id': modele_lines,

        })
        return res

    @api.depends('model_id.total_net')
    def _amount_all(self):
        for time in self:
            amount_cost = amount_advanced = 0.0
            for line in time.model_id:
                # line._compute_amount()
                amount_cost += line.total_cost
                print(amount_cost)
                amount_advanced += (line.advanced_1 + line.advanced_2)
            time.update({
                'amount_cost': amount_cost,
                'amount_advanced': amount_advanced,
                'amount_total': amount_cost - amount_advanced,
            })


    name = fields.Char(string='Nom', store=True, required=True)
    partner_id = fields.Many2one('res.partner', 'Client')
    employee_id = fields.Many2one('hr.employee', string='Employer')
    model_id = fields.One2many('time_sheet_module.model', 'time_id', required=True, auto_join=True)
    date = fields.Date('Date de creation', default=datetime.today())

    month = fields.Selection([
        ('1', 'Janvier'),
        ('2', 'Février'),
        ('3', 'Mars'),
        ('4', 'Avril'),
        ('5', 'Mai'),
        ('6', 'Juin'),
        ('7', 'Juillet'),
        ('8', 'Août'),
        ('9', 'Septembre'),
        ('10', 'Octobre'),
        ('11', 'Novembre'),
        ('12', 'Décember'),
    ], string='Mois', default='1', required=True, store=True)
    year = fields.Selection(get_years(), string='Year', required=True)
    is_fev_29 = fields.Boolean('Février 29', compute='_get_days')
    is_fev_28 = fields.Boolean('Février 28', compute='_get_days')
    is_thirty_one_day = fields.Boolean('31 jours', compute='_get_days')
    is_thirty_day = fields.Boolean('30jours', compute='_get_days')

    amount_cost = fields.Float(string='Côuts', store=False, readonly=True, compute='_amount_all',
                               tracking=True)
    amount_advanced = fields.Float(string='Avances', store=True, readonly=True, compute='_amount_all')
    amount_total = fields.Float(string='Total', store=True, readonly=True, compute='_amount_all')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Le nom doit être unique !')
    ]

    @api.depends('month', 'year')
    def _get_days(self):
        self.is_fev_28 = False
        self.is_fev_29 = False
        self.is_thirty_one_day = False
        self.is_thirty_day = False
        if self.month == '2':
            if (int(self.year) % 4 == 0 and int(self.year) % 100 != 0 or int(self.year) % 400 == 0):
                self.is_fev_29 = True
            else:
                self.is_fev_28 = True

        elif self.month == '1' or self.month == '3' or self.month == '5' or self.month == '7' or self.month == '8' or self.month == '10' or self.month == '12':
            self.is_thirty_one_day = True
        else:
            self.is_thirty_day = True

    @api.constrains('month', 'year')
    def _validate_date(self):
        for r in self:
            existe = self.env['time_sheet_module.time'].search_count(
                ['&', ('partner_id', '=', self.partner_id.id), ('month', '=', self.month), ('year', '=', self.year)])
            if (existe > 1):
                raise exceptions.ValidationError("Date Existe Déja!: \n Année:  " + str(self.year) +
                                                 ' Mois: ' + dict(self._fields['month'].selection).get(self.month))

    @api.model
    def create(self, values):
        """ We don't want the current user to be follower of all created Pointage """
        return super(TimeSheet, self.with_context(mail_create_nosubscribe=True)).create(values)


class model(models.Model):
    _name = 'time_sheet_module.model'
    _rec_name = 'employee_id'

    time_id = fields.Many2one('time_sheet_module.time', string='time_id', required=True, ondelete='cascade', index=True,
                              copy=False)
    month = fields.Selection([
        ('1', 'Janvier'),
        ('2', 'Février'),
        ('3', 'Mars'),
        ('4', 'Avril'),
        ('5', 'Mai'),
        ('6', 'Juin'),
        ('7', 'Juillet'),
        ('8', 'Août'),
        ('9', 'Septembre'),
        ('10', 'Octobre'),
        ('11', 'Novembre'),
        ('12', 'Décember'),
    ], string='Mois', related='time_id.month')
    employee_id = fields.Many2one('hr.employee', string='Employer')

    one = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='1')
    two = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='2')
    three = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='3')
    four = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='4')
    five = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='5')
    seven = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='7')
    six = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='6')
    eight = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='8')
    nine = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='9')
    ten = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='10')
    one_1 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='11')
    one_2 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='12')
    one_3 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='13')
    one_4 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='14')
    one_5 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='15')
    one_6 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='16')
    one_7 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='17')
    one_8 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='18')
    one_9 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='19')
    two_0 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='20')
    two_1 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='21')
    two_2 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='22')
    two_3 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='23')
    two_4 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='24')
    two_5 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='25')
    two_6 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='26')
    two_7 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='27')
    two_8 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='28')
    two_9 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='29')
    three_0 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='30')
    three_1 = fields.Selection([('1', 'Présent'), ('2', 'Absent'), ('3', 'congés'), ('4', 'Demi-journée'), ('5', 'Maladie')], string='31')
    is_fev_29 = fields.Boolean('Février 29', related='time_id.is_fev_29')
    is_fev_28 = fields.Boolean('Février 28', related='time_id.is_fev_28')
    is_thirty_one_day = fields.Boolean('31 jours', related='time_id.is_thirty_one_day')
    is_thirty_day = fields.Boolean('30jours', related='time_id.is_thirty_day')
    cost = fields.Float('Coûts  par jour', )
    advanced_1 = fields.Float('Avance 1', store=True)
    advanced_2 = fields.Float('Avance 2', store=True)
    # total_advanced = fields.Float(compute="_get_total_advanced", string='Total des avances', store=False)

    total_day = fields.Float(compute="_get_total_day", string='Total des jours', store=False)

    total_cost = fields.Float(string='Total coûts', compute="_get_total_cost", store=True)
    total_net = fields.Float(string='Total Net', compute="_get_total_net", store=False)

    @api.depends('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'one_1', 'one_2',
                 'one_3', 'one_4', 'one_5', 'one_6', 'one_7', 'one_8', 'one_9', 'two_0', 'two_1', 'two_2', 'two_3',
                 'two_4', 'two_5', 'two_6', 'two_7', 'two_8', 'two_9', 'two_0', 'three_0', 'three_1')
    # @api.depends('advanced_1', 'advanced_2')
    # def _get_total_advanced(self):
    #     self.total_advanced = self.advanced_1 + self.advanced_2

    def _get_total_day(self):
        for m in self:
            days = []
            if m.one:
                days.append(m.one)
            if m.two:
                days.append(m.two)
            if m.three:
                days.append(m.three)
            if m.four:
                days.append(m.four)
            if m.five:
                days.append(m.five)
            if m.six:
                days.append(m.six)
            if m.seven:
                days.append(m.seven)
            if m.eight:
                days.append(m.eight)
            if m.nine:
                days.append(m.nine)
            if m.ten:
                days.append(m.ten)
            if m.one_1:
                days.append(m.one_1)
            if m.one_2:
                days.append(m.one_2)
            if m.one_3:
                days.append(m.one_3)
            if m.one_4:
                days.append(m.one_4)
            if m.one_5:
                days.append(m.one_5)
            if m.one_6:
                days.append(m.one_6)
            if m.one_7:
                days.append(m.one_7)
            if m.one_8:
                days.append(m.one_8)
            if m.one_9:
                days.append(m.one_9)
            if m.two_0:
                days.append(m.two_0)
            if m.two_1:
                days.append(m.two_1)
            if m.two_2:
                days.append(m.two_2)
            if m.two_3:
                days.append(m.two_3)
            if m.two_4:
                days.append(m.two_4)
            if m.two_5:
                days.append(m.two_5)
            if m.two_6:
                days.append(m.two_6)
            if m.two_7:
                days.append(m.two_7)
            if m.two_8:
                days.append(m.two_8)
            if m.two_9:
                days.append(m.two_9)
            if m.three_0:
                days.append(m.three_0)
            if m.three_1:
                days.append(m.three_1)

            nbr_day = 0.0
            for day in days:
                if day == '1':
                    nbr_day += 1
                elif day == '4':
                    nbr_day += 0.5
            m.total_day = nbr_day

    @api.depends('total_day', 'cost')
    def _get_total_cost(self):
        for m in self:
            m.total_cost = m.total_day * m.cost

    @api.depends('total_cost', 'advanced_1', 'advanced_2')
    def _get_total_net(self):
        for m in self:
            m.total_net = m.total_cost - (m.advanced_1 + m.advanced_2)

    def action_show_model_id_details(self):
        """ Returns an action that will open a form view (in a popup) allowing to work on all the
        model lines of a particular model
        """
        self.ensure_one()
        view = self.env.ref('time_sheet_module.model_view_form')
        return {
            'name': _('Pointage'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'time_sheet_module.model',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': self.id,
        }

    # class PartnerRes(models.Model):
    #     _inherit = 'res.partner'
    #
    #     conducteurs = fields.One2many('condicteur.part', 'parent_id')
    #
    #
    # class PartnerResCond(models.Model):
    #     _name = 'condicteur.part'
    #     # _inherit = 'res.partner'
    #
    #     parent_id = fields.Many2one('res.partner')
    #     ref = fields.Char('')
    #     name = fields.Char('')
