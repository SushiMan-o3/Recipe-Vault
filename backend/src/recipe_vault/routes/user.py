from fastapi import APIRouter, Depends, HTTPException, status
from database import close_connection, create_connection
from schemas.profile import Profile, UpdateAdditionalInfo, UpdateProfilePicture
from services.security import get_current_user

route = APIRouter(
    prefix="/profile",
    tags=["profile"],
)


@route.get("/{user_id}", response_model=Profile)
def get_profile(user_id: int):
    conn, cursor = None, None

    try:
        conn, cursor = create_connection()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        cursor.execute("SELECT * FROM additionaluserinfo WHERE user_id = %s", (user_id,))
        additional_info = cursor.fetchone() or {}

        return Profile(
            user_id=user["id"],
            username=user["username"],
            email=user["email"],
            first_name=additional_info.get("first_name"),
            last_name=additional_info.get("last_name"),
            bio=additional_info.get("bio"),
            birthday=additional_info.get("birthday"),
            gender=additional_info.get("gender"),
            country=additional_info.get("country"),
            profile_picture_url=additional_info.get("profile_picture_url"),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    finally:
        close_connection(conn, cursor)


@route.put("/{user_id}")
def update_profile(
    user_id: int,
    additional_info: UpdateAdditionalInfo,
    current_user: dict = Depends(get_current_user),
):
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile",
        )

    # TODO: write the update logic here


@route.put("/{user_id}/update-profile-picture")
def update_profile_picture(
    user_id: int,
    profile_picture: UpdateProfilePicture,
    current_user: dict = Depends(get_current_user),
):
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile",
        )

    # TODO: write the update logic here


"""
Follow and unfollow system below
"""