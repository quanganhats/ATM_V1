from fastapi import Body, Request, HTTPException, Depends

from app.models import User
from app.services.srv_user import UserService


async def login_required(http_authorization_credentials=Depends(UserService().reusable_oauth2)):
    return await UserService().get_current_user(http_authorization_credentials.credentials)


class PermissionRequired:
    def __init__(self, *args):
        self.user = None
        self.permissions = args

    def __call__(self, user: User = Depends(login_required)):
        self.user = user
        if self.user.role not in self.permissions and self.permissions:
            raise HTTPException(status_code=400,
                                detail=f'User {self.user.role} can not access this api')
