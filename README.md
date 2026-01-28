# UV Copier Template

A Copier template for creating Python projects with `uv` as the package manager.

## Usage

### From GitHub

```bash
copier copy gh:username/uv-copier-template my-project
```

### From local path

```bash
copier copy /path/to/uv-copier-template my-project
```

### Destination behavior

- `copier copy template my-project` → Creates `my-project/` with all generated files
- `copier copy template .` → Generates files directly in current directory
- `copier copy template existing-dir/` → Creates `existing-dir/project-slug/` subdirectory

**Recommended:** Use a new directory name so the project is isolated:

```bash
copier copy gh:username/uv-copier-template my-new-project
```

This will prompt you for project details and create the full project structure in `my-new-project/`.

The template will prompt you for:
- **Project name**: Human-friendly name (e.g., "My Project")
- **Project slug**: Repository slug in kebab-case (auto-generated from project name)
- **Package name**: Python import name in snake_case (auto-generated from slug)
- **Description**: One-line description
- **Author name**: Your name
- **Author email**: Your email
- **Python version**: Minimum Python version (default: 3.11)
- **Project type**: library, cli, api, or ml
- **Include CI**: Add GitHub Actions workflow
- **Include pre-commit**: Add pre-commit configuration
- **License**: MIT or Proprietary

## Features

- ✅ UV package manager setup
- ✅ Pytest configuration
- ✅ Ruff linter and formatter
- ✅ MyPy type checking
- ✅ Example `.env` template for local configuration
- ✅ Pydantic settings module for loading env variables
- ✅ Optional GitHub Actions CI/CD
- ✅ Optional pre-commit hooks
- ✅ Configurable project types (library, CLI, API, ML)

## Project Structure

The template generates projects with:
```
project-slug/
├── src/package_name/     # Main package code
│   └── settings.py       # Pydantic settings loaded from .env/env vars
├── tests/                # Test files
├── pyproject.toml        # Project configuration (uv, pytest, ruff, mypy)
├── .env.example          # Example environment file
├── .pre-commit-config.yaml  # Pre-commit hooks (if enabled)
├── .github/workflows/    # CI/CD workflows (if enabled)
└── README.md            # Generated project README
```

## Development

To test the template locally:

```bash
copier copy . /tmp/test-project
```

To update an existing project with template changes:

```bash
copier update /path/to/project
```
