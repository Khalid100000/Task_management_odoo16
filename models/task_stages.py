from odoo import api, fields, models

class TaskStages(models.Model):
    _name = "task.management.stages"
    _description='Task Stages'
    _order = "sequence"

    name = fields.Char()
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    active = fields.Boolean(default=True)
    fold = fields.Boolean()
    #user_ids = fields.Many2many('res.users', string="Users")# for permissions



