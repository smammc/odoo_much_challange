# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta


class ProjectSprint(models.Model):
    """Sprint management for Agile project management"""
    _name = 'project.sprint'
    _description = 'Project Sprint'
    _order = 'start_date desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    _sql_constraints = [
        ('name_project_uniq', 'UNIQUE(name, project_id)', 
         'Sprint name must be unique per project!'),
    ]

    # Basic Fields
    name = fields.Char(
        string='Sprint Name',
        required=True,
        tracking=True,
        help="Name of the sprint (e.g., 'Sprint 1', 'Q1 Sprint 3')"
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True
    )
    
    project_id = fields.Many2one(
        'project.project',
        string='Project',
        required=True,
        ondelete='cascade',
        tracking=True,
        index=True,
        help="Project this sprint belongs to"
    )
    
    start_date = fields.Date(
        string='Start Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True,
        index=True
    )
    
    end_date = fields.Date(
        string='End Date',
        required=True,
        tracking=True
    )
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('done', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', required=True, tracking=True, index=True)
    
    goal = fields.Text(
        string='Sprint Goal',
        tracking=True,
        help="What the team aims to achieve in this sprint"
    )
    
    task_ids = fields.One2many(
        'project.task',
        'sprint_id',
        string='Tasks'
    )
    
    user_id = fields.Many2one(
        'res.users',
        string='Scrum Master',
        default=lambda self: self.env.user,
        tracking=True
    )
    
    color = fields.Integer(string='Color Index', default=0)
    
    # Computed Fields
    task_count = fields.Integer(
        compute='_compute_task_metrics',
        store=True,
        string='Total Tasks'
    )
    
    completed_task_count = fields.Integer(
        compute='_compute_task_metrics',
        store=True,
        string='Completed Tasks'
    )
    
    progress = fields.Float(
        compute='_compute_task_metrics',
        store=True,
        string='Progress (%)'
    )
    
    story_points_total = fields.Integer(
        compute='_compute_task_metrics',
        store=True,
        string='Total Story Points'
    )
    
    story_points_completed = fields.Integer(
        compute='_compute_task_metrics',
        store=True,
        string='Completed Story Points'
    )
    
    duration_days = fields.Integer(
        compute='_compute_duration',
        store=True,
        string='Duration (Days)'
    )
    
    days_remaining = fields.Integer(
        compute='_compute_days_remaining',
        string='Days Remaining'
    )
    
    velocity = fields.Float(
        compute='_compute_velocity',
        store=True,
        string='Velocity (Points/Day)'
    )
    
    backlog_task_count = fields.Integer(
        compute='_compute_backlog_task_count',
        string='Backlog Tasks'
    )
    
    # Compute Methods
    @api.depends('task_ids', 'task_ids.stage_id', 'task_ids.stage_id.fold', 'task_ids.story_points')
    def _compute_task_metrics(self):
        """Calculate task completion metrics"""
        for sprint in self:
            tasks = sprint.task_ids
            completed = tasks.filtered(lambda t: t.stage_id.fold)
            
            sprint.task_count = len(tasks)
            sprint.completed_task_count = len(completed)
            sprint.progress = (len(completed) / len(tasks) * 100) if tasks else 0.0
            sprint.story_points_total = sum(task.story_points or 0 for task in tasks)
            sprint.story_points_completed = sum(task.story_points or 0 for task in completed)
    
    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        """Calculate sprint duration in days"""
        for sprint in self:
            if sprint.start_date and sprint.end_date:
                delta = sprint.end_date - sprint.start_date
                sprint.duration_days = delta.days + 1
            else:
                sprint.duration_days = 0
    
    @api.depends('end_date', 'state')
    def _compute_days_remaining(self):
        """Calculate days remaining until sprint end"""
        today = fields.Date.context_today(self)
        for sprint in self:
            if sprint.state == 'active' and sprint.end_date:
                delta = sprint.end_date - today
                sprint.days_remaining = max(0, delta.days)
            else:
                sprint.days_remaining = 0
    
    @api.depends('story_points_completed', 'duration_days', 'state')
    def _compute_velocity(self):
        """Calculate velocity for completed sprints"""
        for sprint in self:
            if sprint.state == 'done' and sprint.duration_days > 0:
                sprint.velocity = round(sprint.story_points_completed / sprint.duration_days, 2)
            else:
                sprint.velocity = 0.0
    
    @api.depends('project_id')
    def _compute_backlog_task_count(self):
        """Count available backlog tasks for this project"""
        for sprint in self:
            if sprint.project_id:
                count = self.env['project.task'].search_count([
                    ('project_id', '=', sprint.project_id.id),
                    ('sprint_id', '=', False)
                ])
                sprint.backlog_task_count = count
            else:
                sprint.backlog_task_count = 0
    
    # Constraints
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        """Validate sprint dates"""
        for sprint in self:
            if sprint.start_date and sprint.end_date:
                if sprint.end_date < sprint.start_date:
                    raise ValidationError(_('End date cannot be earlier than start date.'))
                if sprint.duration_days > 30:
                    raise ValidationError(_('Sprint duration should not exceed 30 days.'))
    
    @api.constrains('start_date', 'end_date', 'project_id', 'state')
    def _check_sprint_overlap(self):
        """Prevent overlapping active sprints in the same project"""
        for sprint in self:
            if sprint.state in ('draft', 'active') and sprint.start_date and sprint.end_date:
                domain = [
                    ('id', '!=', sprint.id),
                    ('project_id', '=', sprint.project_id.id),
                    ('state', 'in', ('draft', 'active')),
                    ('start_date', '<=', sprint.end_date),
                    ('end_date', '>=', sprint.start_date),
                ]
                overlapping = self.search(domain, limit=1)
                if overlapping:
                    raise ValidationError(
                        _('Sprint "%s" overlaps with existing sprint "%s" in this project.') 
                        % (sprint.name, overlapping.name)
                    )
    
    # Onchange Methods
    @api.onchange('start_date')
    def _onchange_start_date(self):
        """Auto-set end date to 2 weeks from start"""
        if self.start_date and not self.end_date:
            self.end_date = self.start_date + timedelta(days=13)
    
    # Action Methods
    def action_start(self):
        """Start the sprint"""
        for sprint in self:
            if not sprint.task_ids:
                raise UserError(_('Cannot start a sprint without tasks. Please add tasks first.'))
            sprint.write({'state': 'active'})
            sprint.message_post(body=_('Sprint started'))
        return True
    
    def action_complete(self):
        """Complete the sprint with option to handle incomplete tasks"""
        self.ensure_one()
        incomplete_tasks = self.task_ids.filtered(lambda t: not t.stage_id.fold)
        
        if incomplete_tasks:
            return {
                'name': _('Handle Incomplete Tasks'),
                'type': 'ir.actions.act_window',
                'res_model': 'sprint.complete.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_sprint_id': self.id,
                    'default_task_ids': [(6, 0, incomplete_tasks.ids)],
                }
            }
        
        return self._complete_sprint()
    
    def _complete_sprint(self):
        """Actually complete the sprint"""
        self.write({'state': 'done'})
        self.message_post(
            body=_('Sprint completed with velocity: %.2f points/day') % self.velocity
        )
        return True
    
    def action_cancel(self):
        """Cancel the sprint"""
        self.write({'state': 'cancelled'})
        self.message_post(body=_('Sprint cancelled'))
        return True
    
    def action_draft(self):
        """Reset to draft"""
        self.write({'state': 'draft'})
        return True
    
    def action_view_tasks(self):
        """Open tasks view filtered by this sprint"""
        self.ensure_one()
        return {
            'name': _('Sprint Tasks'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'view_mode': 'kanban,tree,form,calendar',
            'domain': [('sprint_id', '=', self.id)],
            'context': {
                'default_sprint_id': self.id,
                'default_project_id': self.project_id.id,
            }
        }
    
    def action_add_existing_tasks(self):
        """Open wizard to add existing tasks from backlog"""
        self.ensure_one()
        return {
            'name': _('Add Tasks from Backlog'),
            'type': 'ir.actions.act_window',
            'res_model': 'sprint.add.tasks.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sprint_id': self.id,
            }
        }