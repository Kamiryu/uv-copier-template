from pathlib import Path

from copier import run_copy


TEMPLATE_ROOT = Path(__file__).resolve().parents[1]


def render_project(tmp_path: Path, **answers: object) -> Path:
    destination = tmp_path / "generated"
    run_copy(
        str(TEMPLATE_ROOT),
        destination,
        data=answers,
        defaults=True,
        quiet=True,
        unsafe=True,
    )
    return destination


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_cli_api_and_automation_presets_generate_runnable_entrypoints(
    tmp_path: Path,
) -> None:
    cli_project = render_project(tmp_path / "cli", project_type="cli")
    cli_pyproject = read_text(cli_project / "pyproject.toml")
    assert 'requires = ["hatchling"]' in cli_pyproject
    assert 'my-project = "my_project.cli:app"' in cli_pyproject
    assert (cli_project / "src" / "my_project" / "cli.py").is_file()

    api_project = render_project(tmp_path / "api", project_type="api")
    assert (api_project / "src" / "my_project" / "api.py").is_file()
    assert "app = FastAPI" in read_text(api_project / "src" / "my_project" / "api.py")

    automation_project = render_project(
        tmp_path / "automation",
        project_type="automation",
    )
    automation_pyproject = read_text(automation_project / "pyproject.toml")
    assert 'my-project = "my_project.runner:app"' in automation_pyproject
    assert (automation_project / "src" / "my_project" / "runner.py").is_file()
    assert '"httpx>=' in automation_pyproject


def test_data_and_ml_presets_add_expected_dependencies_and_notebooks_by_default(
    tmp_path: Path,
) -> None:
    data_pyproject = read_text(
        render_project(tmp_path / "data", project_type="data") / "pyproject.toml"
    )
    assert '"numpy>=' in data_pyproject
    assert '"pandas>=' in data_pyproject
    assert '"pyarrow>=' in data_pyproject
    assert "notebooks = [" in data_pyproject
    assert '"jupyterlab>=' in data_pyproject

    ml_pyproject = read_text(
        render_project(tmp_path / "ml", project_type="ml") / "pyproject.toml"
    )
    assert '"numpy>=' in ml_pyproject
    assert '"pandas>=' in ml_pyproject
    assert '"scikit-learn>=' in ml_pyproject
    assert "notebooks = [" in ml_pyproject
    assert '"jupyterlab>=' in ml_pyproject


def test_optional_toggles_add_runtime_and_tooling_support(tmp_path: Path) -> None:
    project = render_project(
        tmp_path,
        include_database=True,
        include_docs=True,
        include_http_client=True,
        include_notebooks=True,
    )
    pyproject = read_text(project / "pyproject.toml")
    settings = read_text(project / "src" / "my_project" / "settings.py")

    assert '"httpx>=' in pyproject
    assert '"sqlalchemy>=' in pyproject
    assert '"alembic>=' in pyproject
    assert "docs = [" in pyproject
    assert '"mkdocs-material>=' in pyproject
    assert (project / "mkdocs.yml").is_file()
    assert (project / "docs" / "index.md").is_file()
    assert "notebooks = [" in pyproject
    assert '"jupyterlab>=' in pyproject
    assert 'database_url: str = "sqlite:///./app.db"' in settings
    assert (project / "src" / "my_project" / "database.py").is_file()
    assert (project / "alembic.ini").is_file()
    assert (project / "alembic" / "env.py").is_file()


def test_template_tests_are_not_rendered_into_generated_projects(tmp_path: Path) -> None:
    project = render_project(tmp_path)

    assert not (project / "template_tests").exists()


def test_template_git_metadata_is_not_rendered_into_generated_projects(
    tmp_path: Path,
) -> None:
    project = render_project(tmp_path)

    assert not (project / ".git").exists()


def test_generated_text_files_do_not_contain_unresolved_jinja(tmp_path: Path) -> None:
    project = render_project(
        tmp_path,
        project_type="api",
        include_database=True,
        include_docs=True,
        include_http_client=True,
        include_notebooks=True,
    )
    text_files = [
        path
        for path in project.rglob("*")
        if path.is_file()
        and path.suffix in {".example", ".ini", ".md", ".py", ".toml", ".yaml", ".yml"}
    ]

    for path in text_files:
        content = read_text(path)
        assert "{{" not in content, path
        assert "{%" not in content, path
