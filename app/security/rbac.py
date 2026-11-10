from fastapi import Depends, HTTPException, status

from app.dependencies import get_current_user
from app.models.user import User


def require_role(*allowed_roles: str):

    def role_checker(
        current_user: User = Depends(get_current_user),
    ):
        actual_role = (current_user.role or "").strip().lower()
        normalized_roles = {role.strip().lower() for role in allowed_roles}
        if actual_role not in normalized_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )

        return current_user

    return role_checker
