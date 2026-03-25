# SDS (Super Duper Secret)

### Install:

Install using the latest release package from the 'releases' section.

### Development Setup:

1. Your Python version must be `>=3.13.0`
2. Set up virtual environment(Inside the project directory): 
    - Linux: `python3 -m venv .venv`
    - Windows: `python -m venv .venv`
3. Activate virtual environment: 
    - Linux: `. .venv/bin/activate`
    - Windows: `.\.venv\Scripts\activate`
4. Setup package and dependencies: 
    - Linux: `.venv/bin/pip install -e .`
    - Windows: `pip install -e .`
5. Run the project: 
    - Linux: `.venv/bin/python src/main.py` 
    - Windows: `python src\main.py`
    
### Project Map:

- `pyproject.toml` Contains metadata such as dependencies for the project.
- `data/` Contains the database files.
- `assets/` Contains icons and other non-source-code files.
- `src/` Contains source code for the project.
    - `src/core/` Contains the source code for core functionality such as encryption/hashing.
    - `src/db/` Contains the source code for the database.
    - `src/ui/` Contains the source code for the GUI and CLI.
    - `src/main/` Is the primary entry point (file that is executed to start the application).




