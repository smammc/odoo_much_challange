# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SprintCompleteWizard(models.TransientModel):
    _name = 'sprint.complete.wizard'
    _description = 'Sprint Complete Wizard'

    sprint_id = fields.Many2one(
        'project.sprint',
        string='Sprint',
        required=True,
        readonly=True
    )
    
    task_ids = fields.Many2many(
        'project.task',
        string='Incomplete Tasks',
        readonly=True
    )
    
    action = fields.Selection([
        ('move', 'Move to Next Sprint'),
        ('backlog', 'Move to Backlog'),
        ('keep', 'Keep in Current Sprint'),
    ], string='Action for Incomplete Tasks', default='backlog', required=True)
    
    next_sprint_id = fields.Many2one(
        'project.sprint',
        string='Next Sprint',
        domain="[('project_id', '=', project_id), ('state', '=', 'draft'), ('id', '!=', sprint_id)]"
    )
    
    project_id = fields.Many2one(
        related='sprint_id.project_id',
        string='Project'
    )
    
    incomplete_task_count = fields.Integer(
        compute='_compute_incomplete_task_count',
        string='Incomplete Tasks Count'
    )
    
    @api.depends('task_ids')
    def _compute_incomplete_task_count(self):
        for wizard in self:
            wizard.incomplete_task_count = len(wizard.task_ids)
    
    @api.onchange('action')
    def _onchange_action(self):
        """Clear next_sprint_id if action is not 'move'"""
        if self.action != 'move':
            self.next_sprint_id = False
    
    def action_confirm(self):
        """Process incomplete tasks and complete the sprint"""
        self.ensure_one()
        
        if self.action == 'move':
            if not self.next_sprint_id:
                raise models.ValidationError(_('Please select a sprint to move tasks to.'))
            self.task_ids.write({'sprint_id': self.next_sprint_id.id})
        elif self.action == 'backlog':
            self.task_ids.write({'sprint_id': False})
        # 'keep' action: do nothing, tasks stay in current sprint
        
        return self.sprint_id._complete_sprint()
