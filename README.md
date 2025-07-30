# COMP 353 - MTL Volleyball Club GUI

This project is a web application for managing the database of the MTL Volleyball Club. It uses Flask, Flask-Admin, and SQLAlchemy to provide an admin interface for viewing and managing club members, their locations, hobbies, etc.

## Installation

1. Clone this repository.
2. Install/sync the libraries and environment using [uv](https://github.com/astral-sh/uv):
```
uv sync
```

## Running the Application

1. Set up your database configuration in `src/app.py`.
2. Run the Application
```
uv run -- flask --app src/app.py run --debug -p 3000
```
3. Visit http://127.0.0.1:3001/admin/