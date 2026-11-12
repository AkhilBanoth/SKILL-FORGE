
class SkillForgeException(Exception):
    """Base exception for SkillForge application errors."""

    def __init__(
        self,
        message: str = "An application error occurred.",
    ):
        self.message = message
        super().__init__(message)


class ResourceNotFoundError(SkillForgeException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str = "Resource"):
        super().__init__(f"{resource} was not found.")


class ResourceAlreadyExistsError(SkillForgeException):
    """Raised when a resource already exists."""

    def __init__(self, resource: str = "Resource"):
        super().__init__(f"{resource} already exists.")


class BusinessRuleError(SkillForgeException):
    """Raised when a business rule is violated."""


class PermissionDeniedError(SkillForgeException):
    """Raised when an operation is not permitted."""

    def __init__(
        self,
        message: str = "You do not have permission to perform this action.",
    ):
        super().__init__(message)


class InvalidInputError(SkillForgeException):
    """Raised when application-level input validation fails."""
