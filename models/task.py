from odoo import models, fields,api,_
from odoo.exceptions import ValidationError
from datetime import date

class Task(models.Model):
    _name = 'task.management.task'
    _description = 'Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    #model fields
    name = fields.Char(string='Task Name', required=True)
    description = fields.Text(string='Description',tracking=True)
    date_deadline = fields.Date(string='Deadline',required=True,tracking=True)
    active=fields.Boolean(string='Active',default=True)
    sequence = fields.Char(string='Sequence', readonly=True, copy=False, default=lambda self: _('New'))
    
    #this field is for for the person who created the task and it is automatically defined
    creator = fields.Many2one('res.users', string='Creator',default=lambda self: self.env.user, readonly=True, tracking=True)
    # This field should have been named creator_id
    
    #Stages related
    @api.model
    def _default_stage_id(self):
        """
            This function gives a default stage for the newly created task
        
        """
        Stage = self.env["task.management.stages"] # returns all the record of stges in the database

        return Stage.search([("name", "=", "New")],limit=1) # search for the stage with name "New" to make it as the current stage for the task

    @api.model
    def _group_expand_stage_id(self, stages, domain,order):
        """
        function expands the available options for the stage_id field 
        by retrieving all stage records and applying the provided order.
        
        """
        return stages.search([], order=order)
    
    stage_id = fields.Many2one('task.management.stages', string="Stage",default=_default_stage_id,group_expand="_group_expand_stage_id", tracking=True)


    @api.constrains('date_deadline')
    def _check_value(self):
        for record in self:
            if record.date_deadline < date.today():
                raise ValidationError('Deadline Must be After the current date')

    @api.model
    def create(self, vals):
        #if vals.get('sequence', _('New')) == _('New'): # the comparison here is not mandatory

        vals['sequence'] = self.env['ir.sequence'].next_by_code('task.management.task')
        res = super(Task, self).create(vals)
        return res