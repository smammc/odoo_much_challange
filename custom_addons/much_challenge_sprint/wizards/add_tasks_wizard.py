# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AddTasksWizard(models.TransientModel):
    _name = 'sprint.add.tasks.wizard'
    _description = 'Add Tasks to Sprint Wizard'

    sprint_id = fields.Many2one(
        'project.sprint',
        string='Sprint',
        required=True,
        readonly=True
    )
    
    project_id = fields.Many2one(
        related='sprint_id.project_id',
        string='Project',
        readonly=True
    )
    
    available_task_ids = fields.Many2many(
        'project.task',
        'sprint_add_wizard_task_rel',
        'wizard_id',
        'task_id',
        string='Available Tasks',
        compute='_compute_available_tasks'
    )
    
    task_ids = fields.Many2many(
        'project.task',
        'sprint_add_wizard_selected_task_rel',
        'wizard_id',
        'task_id',
        string='Tasks to Add',
        domain="[('id', 'in', available_task_ids)]"
    )
    
    @api.depends('sprint_id', 'project_id')
    def _compute_available_tasks(self):
        for wizard in self:
            if wizard.project_id:
                # Get tasks from the same project that are not in any sprint
                tasks = self.env['project.task'].search([
                    ('project_id', '=', wizard.project_id.id),
                    ('sprint_id', '=', False)
                ])
                wizard.available_task_ids = tasks
            else:
                wizard.available_task_ids = False
    
    def action_add_tasks(self):
        """Add selected tasks to the sprint"""
        self.ensure_one()
        if self.task_ids:
            self.task_ids.write({'sprint_id': self.sprint_id.id})
        return {'type': 'ir.actions.act_window_close'}