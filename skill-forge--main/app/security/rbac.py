from fastapi import Depends, HTTPException, status

from app.dependencies import get_current_user
from app.models.user import User


def require_role(*allowed_roles: str):
    """Require one of the allowed roles for a given route."""

    def role_checker(
        current_user: User = Depends(get_current_user),
    ):
        actual_role = (current_user.role or "").strip().lower()
        normalized_roles = {role.strip().lower() for role in allowed_roles}
        if actual_role not in normalized_roles:
            if "admin" in normalized_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Admin access required",
                )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )

        return current_user

    return role_checker


def require_admin_or_mentor():
    return require_role("admin", "mentor")


def require_admin_or_owner(owner_id_getter):
    def checker(
        current_user: User = Depends(get_current_user),
    ):
        actual_role = (current_user.role or "").strip().lower()
        if actual_role == "admin":
            return current_user

        owner_id = owner_id_getter(current_user)
        if owner_id == current_user.id:
            return current_user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )

    return checker
