from fastapi import APIRouter, HTTPException, status, Form
from database import close_connection, create_connection
from schemas.profile import Profile, UpdateAdditionalInfo, UpdateProfilePicture

route = APIRouter(
    prefix="/profile",
    tags=["profile"],
)


@route.get("/{user_id}", response_model=Profile)
def get_profile(userid: int):
    if not userid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID is required",
        )

    try:
        conn, cursor = create_connection()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (userid,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        cursor.execute("SELECT * FROM additionaluserinfo WHERE user_id = %s", (userid,))
        additional_info = cursor.fetchone()

        """
        Get the profile picture URL from the database if it exists, otherwise set it to None
        Get all user information and return it as a Profile object
        Get all recipes created by the user and return them as a list of Recipe objects
        """

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
def update_profile(userid: int, additional_info: UpdateAdditionalInfo, UserModel = Depends(get_current_user)):
    if not userid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID is required",
        )
        
    if current_user["user_id"] != userid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )


    try:
        conn, cursor = create_connection()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (userid,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        cursor.execute("SELECT * FROM additionaluserinfo WHERE user_id = %s", (userid,))
        additional_info = cursor.fetchone()

        if not additional_info:
            cursor.execute(
                "INSERT INTO additionaluserinfo (user_id, first_name, last_name, bio, birthday, gender, country) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    userid,
                    additional_info.first_name,
                    additional_info.last_name,
                    additional_info.bio,
                    additional_info.birthday,
                    additional_info.gender,
                    additional_info.country,
                ),
            )
            additional_info = cursor.fetchone()
            conn.commit()


    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    finally:
        close_connection(conn, cursor)


@route.put("/{user_id}/update-profile-picture")
def update_profile_picture(userid: int, profile_picture: UpdateProfilePicture):
    pass


"""
Follow and unfollow system below
"""