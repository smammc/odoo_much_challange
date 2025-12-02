# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    sprint_id = fields.Many2one(
        'project.sprint',
        string='Sprint',
        ondelete='set null',
        tracking=True,
        index=True,
        help="Sprint this task belongs to",
        domain="[('project_id', '=', project_id), ('state', 'in', ['draft', 'active'])]"
    )
    
    sprint_state = fields.Selection(
        related='sprint_id.state',
        string='Sprint Status',
        store=True,
        readonly=True
    )
    
    story_points = fields.Integer(
        string='Story Points',
        default=0,
        tracking=True,
        help="Estimated effort using Fibonacci sequence (1, 2, 3, 5, 8, 13, 21)"
    )
    
    @api.constrains('sprint_id', 'project_id')
    def _check_sprint_project_consistency(self):
        """Ensure task and sprint belong to the same project"""
        for task in self:
            if task.sprint_id and task.project_id:
                if task.sprint_id.project_id != task.project_id:
                    raise ValidationError(
                        _('Task "%s" cannot be assigned to sprint "%s" from a different project.')
                        % (task.name, task.sprint_id.name)
                    )
