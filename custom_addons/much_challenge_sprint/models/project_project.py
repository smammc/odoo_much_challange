# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProjectProject(models.Model):
    _inherit = 'project.project'

    sprint_ids = fields.One2many(
        'project.sprint',
        'project_id',
        string='Sprints'
    )
    
    sprint_count = fields.Integer(
        compute='_compute_sprint_count',
        string='Sprint Count'
    )
    
    active_sprint_id = fields.Many2one(
        'project.sprint',
        compute='_compute_active_sprint',
        string='Active Sprint'
    )
    
    @api.depends('sprint_ids')
    def _compute_sprint_count(self):
        for project in self:
            project.sprint_count = len(project.sprint_ids)
    
    @api.depends('sprint_ids', 'sprint_ids.state')
    def _compute_active_sprint(self):
        for project in self:
            active_sprint = project.sprint_ids.filtered(lambda s: s.state == 'active')
            project.active_sprint_id = active_sprint[0] if active_sprint else False
    
    def action_view_sprints(self):
        """Open sprints view filtered by this project"""
        self.ensure_one()
        return {
            'name': _('Sprints'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.sprint',
            'view_mode': 'kanban,tree,form,calendar',
            'domain': [('project_id', '=', self.id)],
            'context': {
                'default_project_id': self.id,
            }
        }
