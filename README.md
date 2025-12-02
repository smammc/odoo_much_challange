# Much Challenge - Odoo 16 Sprint Management Module

A comprehensive Agile Sprint Management module for Odoo 16 that extends the Project application with sprint planning, task management, and velocity tracking capabilities.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Installation Guide](#installation-guide)
5. [Models Documentation](#models-documentation)
6. [Views Documentation](#views-documentation)
7. [Security Configuration](#security-configuration)
8. [Wizards](#wizards)
9. [Technical Decisions](#technical-decisions)

---

## Project Overview

### Purpose

This project was developed as part of the Much Challenge to demonstrate proficiency in Odoo 16 development. The module adds Agile/Scrum sprint management functionality to Odoo's existing Project module, enabling teams to:

- Organize work into time-boxed sprints
- Track progress and team velocity
- Manage task backlogs
- Estimate effort using story points

### Technology Stack

| Component | Version |
|-----------|---------|
| Odoo | 16.0 Community Edition |
| Python | 3.9+ |
| PostgreSQL | 18 |
| Platform | macOS (Homebrew) |

---

## Features

### Core Features

| Feature | Description |
|---------|-------------|
| Sprint Management | Create, edit, and manage sprints with start/end dates |
| Sprint States | Draft → Active → Completed/Cancelled workflow |
| Task Assignment | Assign existing tasks or create new tasks within sprints |
| Story Points | Estimate task effort using story points |
| Progress Tracking | Real-time progress calculation based on completed tasks |
| Velocity Metrics | Automatic velocity calculation for completed sprints |
| Sprint Overlap Prevention | Validation to prevent overlapping sprints in the same project |

### User Interface Features

| Feature | Description |
|---------|-------------|
| Kanban View | Visual sprint board grouped by status |
| List View | Table with list of Sprints
| Calendar View | Timeline view of sprints |
| Smart Buttons | Quick access to tasks and backlog |
| Add Tasks Wizard | User-friendly popup to add existing tasks to sprints |
| Sprint Completion Wizard | Handle incomplete tasks when completing a sprint |

---

## Project Structure
```
much_challenge/
├── config
│ └── odoo.conf # Odoo configuration file
├── custom_addons/
│ └── much_challenge_sprint/ # Sprint management module
│ ├── init.py # Package initializer
│ ├── manifest.py # Module manifest
│ ├── models/
│ │ ├── init.py # Models package initializer
│ │ ├── project_sprint.py # Sprint model
│ │ ├── project_task.py # Task model extension
│ │ └── project_project.py # Project model extension
│ ├── views/
│ │ ├── project_sprint_views.xml # Sprint views
│ │ ├── project_task_views.xml # Task view extensions
│ │ ├── project_project_views.xml # Project view extensions
│ │ └── menu_views.xml # Menu definitions
│ ├── wizards/
│ │ ├── init.py # Wizards package initializer
│ │ ├── sprint_complete_wizard.py # Sprint completion wizard
│ │ ├── sprint_complete_wizard_views.xml # Completion wizard view
│ │ ├── add_tasks_wizard.py # Add tasks wizard
│ │ └── add_tasks_wizard_views.xml # Add tasks wizard view
│ └── security/
│ ├── ir.model.access.csv # Access control list
│ └── project_sprint_security.xml # Security rules
├── data/ # Odoo filestore
├── logs/ # Log files
├── src/
│ └── odoo/ # Odoo 16 source code
├── much_challenge_venv/ # Python virtual environment
└── README.md # This file
```

### Directory Explanations

| Directory | Purpose |
|-----------|---------|
| `config/` | Contains Odoo server configuration including database credentials and paths |
| `custom_addons/` | Custom module development directory, added to Odoo's addons path |
| `custom_addons/much_challenge_sprint/` | The main sprint management module |
| `custom_addons/much_challenge_sprint/models/` | Python model definitions (business logic) |
| `custom_addons/much_challenge_sprint/views/` | XML view definitions (user interface) |
| `custom_addons/much_challenge_sprint/wizards/` | Transient models for popup dialogs |
| `custom_addons/much_challenge_sprint/security/` | Access rights and record rules |
| `data/` | Odoo filestore for attachments, sessions, and assets |
| `logs/` | Application log files for debugging |
| `src/odoo/` | Odoo 16 source code cloned from GitHub |
| `much_challenge_venv/` | Isolated Python virtual environment |

### File Explanations

| File | Purpose |
|------|---------|
| `__init__.py` | Python package initializer, imports submodules |
| `__manifest__.py` | Module metadata: name, version, dependencies, data files |
| `project_sprint.py` | Main sprint model with fields, methods, and constraints |
| `project_task.py` | Extends task model with sprint_id and story_points |
| `project_project.py` | Extends project model with sprint relationships |
| `project_sprint_views.xml` | Tree, form, kanban, calendar, and search views for sprints |
| `project_task_views.xml` | Inherited views to add sprint fields to tasks |
| `project_project_views.xml` | Inherited views to add sprint button to projects |
| `menu_views.xml` | Menu item definition for Sprints |
| `sprint_complete_wizard.py` | Wizard to handle incomplete tasks on sprint completion |
| `add_tasks_wizard.py` | Wizard to select and add backlog tasks to sprint |
| `ir.model.access.csv` | Defines CRUD permissions per user group |
| `project_sprint_security.xml` | Defines record-level security rules |

---

## Installation Guide

### Prerequisites

- Python 3.9 or higher
- PostgreSQL 14 or higher
- Git
- Homebrew (for macOS)

### Step-by-Step Installation

#### 1. Create Project Directory

```bash
mkdir -p ~/much_challenge
cd ~/much_challenge
mkdir -p src custom_addons config logs data
```

#### 2. Create Virtual Environment

```bash

python3 -m venv much_challenge_venv
source much_challenge_venv/bin/activate
pip install --upgrade pip wheel setuptools
```

#### 3. Clone Odoo 16

```bash

cd ~/much_challenge/src
git clone https://github.com/odoo/odoo.git --depth 1 --branch 16.0 --single-branch odoo
```

#### 4. Install Python Dependencies

```bash

cd ~/much_challenge
source much_challenge_venv/bin/activate

# Install Odoo requirements
pip install -r src/odoo/requirements.txt

# Install additional required packages
pip install lxml_html_clean
pip install werkzeug==2.0.2
pip install urllib3==1.26.15
pip install setuptools==68.0.0
```

#### 5. Create PostgreSQL User and Database

```bash

# Create user (enter password when prompted)
createuser --createdb --pwprompt much_challenge_user

# Create database
createdb -U much_challenge_user much_challenge_db
```

#### 6. Configure Odoo

Create the configuration file at config/odoo.conf:

```ini

[options]
; Database settings
db_host = localhost
db_port = 5432
db_user = much_challenge_user
db_password = much_challenge_user
db_name = much_challenge_db

; Paths (update with your actual path)
addons_path = /Users/YOUR_USERNAME/much_challenge/src/odoo/addons,/Users/YOUR_USERNAME/much_challenge/custom_addons
data_dir = /Users/YOUR_USERNAME/much_challenge/data

; Server settings
http_port = 8069
admin_passwd = much_challenge_admin

; Logging
logfile = /Users/YOUR_USERNAME/much_challenge/logs/odoo.log
log_level = info

; Development
dev_mode = reload,xml
```

#### 7. Initialize Database

```bash

cd ~/much_challenge
source much_challenge_venv/bin/activate

# Initialize with base module
python src/odoo/odoo-bin \
    -c config/odoo.conf \
    -d much_challenge_db \
    -i base \
    --stop-after-init
```

#### 8. Install Sprint Module

```bash

python src/odoo/odoo-bin \
    -c config/odoo.conf \
    -d much_challenge_db \
    -i project,much_challenge_sprint \
    --stop-after-init
```

#### 9. Start Odoo Server

```bash

python src/odoo/odoo-bin -c config/odoo.conf
```

#### 10. Access the Application

Open your browser and navigate to: http://localhost:8069

Default login credentials:

    Email: admin
    Password: admin (set on first login)

### Upgrading the Module

After making changes to the module, upgrade it with:

```bash

python src/odoo/odoo-bin \
    -c config/odoo.conf \
    -d much_challenge_db \
    -u much_challenge_sprint \
    --stop-after-init
```

## Models Documentation

### project.sprint

The main sprint model that manages sprint lifecycle.

#### Basic Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | Char | Yes | Sprint name (e.g., "Sprint 1") |
| `project_id` | Many2one | Yes | Related project |
| `company_id` | Many2one | Yes | Company (auto-set from default) |
| `start_date` | Date | Yes | Sprint start date |
| `end_date` | Date | Yes | Sprint end date |
| `state` | Selection | Yes | Status: draft/active/done/cancelled |
| `goal` | Text | No | Sprint goal description |
| `user_id` | Many2one | No | Scrum Master |
| `color` | Integer | No | Color index for kanban view |

#### Relational Fields

| Field | Type | Description |
|-------|------|-------------|
| `task_ids` | One2many | Tasks assigned to this sprint |

#### Computed Fields

| Field | Type | Stored | Description |
|-------|------|--------|-------------|
| `task_count` | Integer | Yes | Total number of tasks |
| `completed_task_count` | Integer | Yes | Number of completed tasks |
| `progress` | Float | Yes | Completion percentage (0-100) |
| `story_points_total` | Integer | Yes | Sum of all task story points |
| `story_points_completed` | Integer | Yes | Sum of completed task story points |
| `duration_days` | Integer | Yes | Sprint duration in days |
| `days_remaining` | Integer | No | Days until sprint end (active only) |
| `velocity` | Float | Yes | Points per day (completed only) |
| `backlog_task_count` | Integer | No | Available backlog tasks count |

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `action_start()` | None | True | Starts the sprint, requires tasks |
| `action_complete()` | None | Action/True | Completes sprint, opens wizard if incomplete tasks |
| `_complete_sprint()` | None | True | Internal method to finalize completion |
| `action_cancel()` | None | True | Cancels the sprint |
| `action_draft()` | None | True | Resets sprint to draft state |
| `action_view_tasks()` | None | Action | Opens tasks view filtered by sprint |
| `action_add_existing_tasks()` | None | Action | Opens wizard to add backlog tasks |

#### Constraints

| Constraint | Type | Description |
|------------|------|-------------|
| `name_project_uniq` | SQL | Sprint name must be unique per project |
| `_check_dates` | Python | End date must be after start date |
| `_check_dates` | Python | Duration cannot exceed 30 days |
| `_check_sprint_overlap` | Python | No overlapping active/draft sprints |

#### Onchange Methods

| Method | Trigger | Description |
|--------|---------|-------------|
| `_onchange_start_date` | start_date | Auto-sets end date to 2 weeks from start |

---

### project.task (Extended)

Extensions to Odoo's standard task model.

#### New Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `sprint_id` | Many2one | No | Assigned sprint |
| `sprint_state` | Selection | No | Related sprint status (readonly) |
| `story_points` | Integer | No | Effort estimation (default: 0) |

#### Constraints

| Constraint | Type | Description |
|------------|------|-------------|
| `_check_sprint_project_consistency` | Python | Task and sprint must belong to same project |

---

### project.project (Extended)

Extensions to Odoo's standard project model.

#### New Fields

| Field | Type | Description |
|-------|------|-------------|
| `sprint_ids` | One2many | All sprints for this project |
| `sprint_count` | Integer | Number of sprints (computed) |
| `active_sprint_id` | Many2one | Currently active sprint (computed) |

#### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `action_view_sprints()` | Action | Opens sprints view filtered by project |

---

## Views Documentation

### Sprint Views

| View ID | Type | Description |
|---------|------|-------------|
| `view_project_sprint_tree` | Tree | List view with columns for key sprint data |
| `view_project_sprint_form` | Form | Complete sprint editing interface |
| `view_project_sprint_kanban` | Kanban | Visual board grouped by state |
| `view_project_sprint_calendar` | Calendar | Timeline view showing sprint duration |
| `view_project_sprint_search` | Search | Filters and grouping options |


### Task View Extensions

| Original View | Extension | Changes |
|---------------|-----------|---------|
| `view_task_form2` | `view_task_form_inherit_sprint` | Added sprint_id and story_points fields |
| `view_task_tree2` | `view_task_tree_inherit_sprint` | Added sprint and story_points columns |
| `view_task_search_form` | `view_task_search_inherit_sprint` | Added sprint filter and grouping |

### Project View Extensions

| Original View | Extension | Changes |
|---------------|-----------|---------|
| `edit_project` | `view_project_form_inherit_sprint` | Added Sprints smart button |
| `view_project_kanban` | `view_project_kanban_inherit_sprint` | Added active sprint display |

---

## Security Configuration

### Access Control List (ir.model.access.csv)

| ID | Model | Group | Read | Write | Create | Delete |
|----|-------|-------|------|-------|--------|--------|
| `access_project_sprint_user` | project.sprint | Project User | ✓ | ✗ | ✗ | ✗ |
| `access_project_sprint_manager` | project.sprint | Project Manager | ✓ | ✓ | ✓ | ✓ |
| `access_sprint_complete_wizard_manager` | sprint.complete.wizard | Project Manager | ✓ | ✓ | ✓ | ✓ |
| `access_sprint_add_tasks_wizard_user` | sprint.add.tasks.wizard | Project User | ✓ | ✓ | ✓ | ✓ |

### Record Rules

| Rule | Model | Groups | Access | Domain |
|------|-------|--------|--------|--------|
| `sprint_rule_user` | project.sprint | Project User | Read | Visible projects only |
| `sprint_rule_manager` | project.sprint | Project Manager | Full | All records |

### Security Design Decisions

1. **Project Users** can view sprints but cannot modify them
2. **Project Managers** have full CRUD access to sprints
3. **Wizards** are accessible based on the operation context
4. **Record rules** respect project visibility settings

---

## Wizards

### Sprint Complete Wizard

**Model:** `sprint.complete.wizard`

**Purpose:** Provides options for handling incomplete tasks when completing a sprint.

#### Fields

| Field | Type | Description |
|-------|------|-------------|
| `sprint_id` | Many2one | The sprint being completed |
| `project_id` | Many2one | Related project (from sprint) |
| `task_ids` | Many2many | Incomplete tasks |
| `action` | Selection | What to do with incomplete tasks |
| `next_sprint_id` | Many2one | Target sprint (if moving tasks) |
| `incomplete_task_count` | Integer | Number of incomplete tasks |

#### Action Options

| Value | Label | Description |
|-------|-------|-------------|
| `move` | Move to Next Sprint | Reassign tasks to selected sprint |
| `backlog` | Move to Backlog | Remove sprint assignment |
| `keep` | Keep in Current Sprint | Leave tasks unchanged |

---

### Add Tasks Wizard

**Model:** `sprint.add.tasks.wizard`

**Purpose:** Provides a user-friendly interface to select and add existing backlog tasks to a sprint.

#### Fields

| Field | Type | Description |
|-------|------|-------------|
| `sprint_id` | Many2one | Target sprint |
| `project_id` | Many2one | Related project (computed) |
| `available_task_ids` | Many2many | All backlog tasks (computed) |
| `task_ids` | Many2many | Selected tasks to add |

---

## Technical Decisions

### Why Extend Existing Models?

**Decision:** Extend `project.task` and `project.project` rather than creating separate linking models.

**Reasons:**
- Seamless integration with existing Odoo functionality
- Leverages existing views, security, and workflows
- Familiar UX for Odoo users
- Less code to maintain
- Better performance (fewer joins)

### Why Use Wizards for Task Selection?

**Decision:** Use transient models (wizards) for adding tasks and completing sprints.

**Reasons:**
- Better UX for complex multi-step operations
- Clear separation between browsing and selecting
- Ability to show comprehensive task information
- Follows Odoo conventions
- Doesn't pollute the main model with temporary data

### Why Prevent Sprint Overlap?

**Decision:** Enforce no overlapping draft/active sprints in the same project.

**Reasons:**
- Clear task ownership at any time
- Accurate velocity calculations
- Proper resource allocation
- Scrum methodology compliance
- Avoids confusion about which sprint tasks belong to

### Why Store Computed Fields?

**Decision:** Store fields like `task_count`, `progress`, `story_points_total`.

**Reasons:**
- Better performance for list views and reporting
- Enables database-level filtering and sorting
- Reduces computation overhead on page load
- Allows use in search domains

### Odoo 16 Compatibility Choices

| Choice | Reason |
|--------|--------|
| Used `attrs` syntax | Required for Odoo 16 view visibility |
| Added `company_id` to views | Required by Odoo 16's view validation for project_id domain |
| Used `column_invisible` in tree | Odoo 16 syntax for hiding columns |
| Bootstrap 5 classes in kanban | Odoo 16 uses Bootstrap 5 |

### Security Model Design

**Decision:** Two-tier security with users (read) and managers (full).

**Reasons:**
- Matches Odoo project module pattern
- Simple and understandable
- Allows team visibility while protecting data
- Managers control sprint lifecycle
