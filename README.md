# IT Task Manager

A Django-based task management application designed for a factory environment.

The project was created as a learning project while developing practical skills in Django, authentication, permissions, relationships, templates, Bootstrap and database management.

## Features

- User authentication and logout
- Role-based permissions
- Worker hierarchy with supervisors
- Personal worker profiles
- Task management
- Task Types
- Positions and Groups
- Multiple assignees per task
- Task priorities
- Task deadlines
- Completed task history
- Responsive Bootstrap 5.3 interface
- Permission-aware navigation
- Demo database included as a JSON fixture

### Dashboard

- Active Tasks
- Completed Today
- Overdue Tasks

## User Roles

The demo database contains several levels of responsibility:

- CEO
- Management
- Supervisor
- Worker
- Specialist

Users can see and access information according to their permissions and position in the company hierarchy.

Workers can always access their own profile, while access to other workers depends on permissions.

## Repository

[GitHub Repository](https://github.com/Qbaldo/IT_task_manager)

## Requirements

- Python
- Django 6.0.5

## Installation

Clone the repository:

git clone https://github.com/Qbaldo/IT_task_manager.git
cd IT_task_manager

Create and activate a virtual environment.

## Windows

python -m venv venv
venv\Scripts\activate

Install Django:

pip install Django==6.0.5

Run migrations:

python manage.py migrate

## Demo database

The repository contains demo_data.json.

Load the demo database with:

python manage.py loaddata demo_data.json

The demo database contains:

- Demo users
- Positions
- Groups and permissions
- Task Types
- 25 example tasks
- Task assignments
- Active and completed tasks
- Overdue tasks
- Tasks with multiple assignees

All demo accounts use the temporary password:

Demo123!

For a real production environment, users should change their temporary password after the first login.

## Running The Application

Start the development server:

python manage.py runserver

Then open:

http://127.0.0.1:8000/

## Demo Users

The demo database includes users representing different roles in the factory hierarchy.

Example:

CEO:
anderson

Supervisor:
miller

Worker:
kowalski

Specialist:
swiecicki

Demo password:

Demo123!

A Django superuser is also included for administration purposes.

## Project status

The first version focuses on the core functionality of task management, users, hierarchy and permissions.

Future ideas may include:

Supervisor dashboards
Improved team management
QR-based user identification
Additional reporting
Improved employee onboarding

These features are intentionally outside the scope of V1.0.