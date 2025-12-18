from AIFoundationKit.base.exception.custom_exception import (
    AppException,
    ResourceNotFoundException,
    ValidationException,
    AuthenticationException,
    PermissionDeniedException,
    DatabaseException,
    ConfigException,
    ModelException,
)


def test_app_exception_to_dict():
    exc = AppException("Error message", code="TEST_CODE", details={"key": "val"})
    data = exc.to_dict()
    assert data["error"]["code"] == "TEST_CODE"
    assert data["error"]["message"] == "Error message"
    assert data["error"]["details"] == {"key": "val"}


def test_subclasses():
    exc = ResourceNotFoundException("Not found")
    assert exc.code == "RESOURCE_NOT_FOUND"
    assert exc.status_code == 404

    exc = ValidationException("Invalid")
    assert exc.code == "VALIDATION_ERROR"
    assert exc.status_code == 400

    exc = AuthenticationException("Auth failed")
    assert exc.code == "AUTHENTICATION_FAILED"
    assert exc.status_code == 401

    exc = PermissionDeniedException("Denied")
    assert exc.code == "PERMISSION_DENIED"
    assert exc.status_code == 403

    exc = DatabaseException("DB Error")
    assert exc.code == "DATABASE_ERROR"
    assert exc.status_code == 500

    exc = ConfigException("Config Error")
    assert exc.code == "CONFIGURATION_ERROR"
    assert exc.status_code == 500

    exc = ModelException("Model Error")
    assert exc.code == "MODEL_ERROR"
    assert exc.status_code == 500
