
import pytest
from pydantic import ValidationError

from app.core.config import AppEnvironment, Settings


@pytest.fixture(autouse=True)
def isolate_settings(monkeypatch):
    """Prevent external environment variables from affecting tests."""
    for name in (
        "APP_NAME",
        "APP_ENV",
        "DATABASE_URL",
        "JWT_SECRET",
        "JWT_ALGORITHM",
        "JWT_EXPIRATION_MINUTES",
        "JWT_REFRESH_EXPIRATION_MINUTES",
        "MAX_FILE_SIZE",
        "ALLOWED_CONTENT_TYPES",
        "ALLOWED_EXTENSIONS",
    ):
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def valid_settings():
    """Provide explicit valid settings for tests."""
    return {
        "app_env": AppEnvironment.DEVELOPMENT,
        "database_url": "sqlite:///./test.db",
        "jwt_secret": "test-secret-" + "x" * 48,
    }


def test_development_accepts_valid_settings(valid_settings):
    settings = Settings(_env_file=None, **valid_settings)

    assert settings.app_env == AppEnvironment.DEVELOPMENT


def test_test_environment_accepts_valid_settings(valid_settings):
    valid_settings["app_env"] = AppEnvironment.TEST

    settings = Settings(_env_file=None, **valid_settings)

    assert settings.app_env == AppEnvironment.TEST


def test_production_accepts_valid_secret(valid_settings):
    valid_settings["app_env"] = AppEnvironment.PRODUCTION

    settings = Settings(_env_file=None, **valid_settings)

    assert settings.app_env == AppEnvironment.PRODUCTION
    assert len(settings.jwt_secret) >= 32


@pytest.mark.parametrize(
    "secret",
    [
        "",
        "weak-secret",
        "CHANGE-ME-SET-IN-ENV-FILE",
        "x" * 31,
    ],
)
def test_production_rejects_invalid_secret(valid_settings, secret):
    valid_settings["app_env"] = AppEnvironment.PRODUCTION
    valid_settings["jwt_secret"] = secret

    with pytest.raises(ValidationError):
        Settings(_env_file=None, **valid_settings)


def test_invalid_environment_is_rejected(valid_settings):
    valid_settings["app_env"] = "invalid-environment"

    with pytest.raises(ValidationError):
        Settings(_env_file=None, **valid_settings)


@pytest.mark.parametrize(
    "required_field",
    ["app_env", "database_url", "jwt_secret"],
)
def test_missing_required_fields_are_rejected(
    valid_settings, required_field
):
    valid_settings.pop(required_field)

    with pytest.raises(ValidationError) as exc_info:
        Settings(_env_file=None, **valid_settings)

    assert any(
        error["loc"] == (required_field,)
        for error in exc_info.value.errors()
    )


def test_environment_variables_are_loaded(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./env.db")
    monkeypatch.setenv("JWT_SECRET", "secure-" + "x" * 48)

    settings = Settings(_env_file=None)

    assert settings.app_env == AppEnvironment.PRODUCTION
    assert settings.database_url == "sqlite:///./env.db"


def test_environment_variables_override_dotenv(monkeypatch, tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "APP_ENV=development\n"
        "DATABASE_URL=sqlite:///./dotenv.db\n"
        "JWT_SECRET=dotenv-secret-" + "x" * 48 + "\n",
        encoding="utf-8",
    )

    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./system.db")
    monkeypatch.setenv("JWT_SECRET", "system-secret-" + "x" * 48)

    settings = Settings(_env_file=env_file)

    assert settings.app_env == AppEnvironment.PRODUCTION
    assert settings.database_url == "sqlite:///./system.db"
    assert settings.jwt_secret.startswith("system-secret-")
