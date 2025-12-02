# -*- coding: utf-8 -*-
{
    'name': 'Sprint Management',
    'version': '16.0.1.0.0',
    'category': 'Project Management',
    'summary': 'Agile Sprint Management for Projects',
    'description': """
Sprint Management Module
========================

This module extends the Project module to add Agile Sprint functionality.

Features
--------
* Create and manage sprints within projects
* Assign tasks to sprints
* Track sprint progress and velocity
* Story points estimation
* Sprint completion workflow with incomplete task handling
* Sprint overlap validation
* Project-sprint consistency checks
    """,
    'author': 'Sebastião Maia Cerqueira',
    'website': 'https://muchchallenge.com',
    'license': 'LGPL-3',
    'depends': [
        'project',
        'mail',
    ],
    'data': [
        # Security first
        'security/project_sprint_security.xml',
        'security/ir.model.access.csv',
        
        # Views
        'views/project_sprint_views.xml',
        'views/project_task_views.xml',
        'views/project_project_views.xml',
        'wizards/sprint_complete_wizard_views.xml',
        
        # Menu last
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
