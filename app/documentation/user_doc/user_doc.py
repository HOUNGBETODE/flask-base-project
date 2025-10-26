add_admin_doc = """
    Add a new administrator.
    ---
    tags:
      - Administration
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - firstname
            - lastname
            - email
            - username
          properties:
            firstname:
              type: string
              description: User's first name
            lastname:
              type: string
              description: User's last name
            username:
              type: string
              description: User's username on the platform
            email:
              type: string
              format: email
              description: User's email address
    responses:
      201:
        description: Administrator account added successfully
      400:
        description: Invalid email address
      422:
        description: Validation error - Required fields missing
      500:
        description: Server error during administrator addition
"""

update_user_doc = """
    Update user information / Also used to edit a user's profile.
    ---
    tags:
      - User
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: UpdateUser
          properties:
            firstname:
              type: string
              description: User's new first name
            lastname:
              type: string
              description: User's new last name
            username:
              type: string
              description: User's username on the platform
            email:
              type: string
              description: User's email address
            gender:
              type: string
              enum: [male, female]
              description: User's gender
    responses:
      200:
        description: Update performed successfully
        schema:
          id: User
          type: object
          properties:
            id:
              type: string
              description: "Unique identifier of the user."
            email:
              type: string
              format: email
              description: "User's email address."
            firstname:
              type: string
              description: "User's first name."
            lastname:
              type: string
              description: "User's last name."
            notifications_count:
              type: integer
              description: "Total number of unread notifications for the user. This field represents notifications that the user has not yet marked as read in the application."
              default: 0
            is_password_set:
              type: boolean
              description: "Indicates if the user has set their password in the application."
            is_google_authenticated:
              type: boolean
              description: "Indicates if the user is authenticated via Google."
            avatar:
              type: string
              description: "User's avatar URL."
            created_at:
              type: string
              format: date-time
              description: "Account creation date."
            updated_at:
              type: string
              format: date-time
              description: "Date of the last update of user information."
      400:
        description: Validation error - Email unavailable or update impossible
      500:
        description: Server error during account update
"""

get_user_profile_doc = """
    Retrieve the authenticated user's profile data.
    ---
    tags:
      - User
    responses:
      200:
        description: User data retrieved successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              description: "Response message."
            success:
              type: boolean
              description: "Indicates whether the request was successful."
            data:
              type: object
              properties:
                id:
                  type: string
                  description: "Unique identifier of the user."
                email:
                  type: string
                  format: email
                  description: "User's email address."
                username:
                  type: string
                  description: "Unique username chosen by the user."
                firstname:
                  type: string
                  description: "User's first name."
                lastname:
                  type: string
                  description: "User's last name."
                avatar:
                  type: string
                  format: uri
                  description: "URL of the user's avatar."
                gender:
                  type: string
                  enum: [male, female]
                  description: "User's gender."
                role:
                  type: string
                  enum: [user, admin, super_admin]
                  description: "Role assigned to the user (e.g., user, admin)."
                notifications_count:
                  type: integer
                  default: 0
                  description: "Total number of unread notifications for the user."
                is_password_set:
                  type: boolean
                  description: "Indicates whether the user has set a password."
                is_google_authenticated:
                  type: boolean
                  description: "Indicates if the user authenticated using Google."
                temporal_password_in_use:
                  type: boolean
                  description: "Indicates whether the user is currently using a temporary password."
                is_verified:
                  type: boolean
                  description: "Indicates if the user's email has been verified."
                is_active:
                  type: boolean
                  description: "Indicates if the user account is active."
                is_admin:
                  type: boolean
                  description: "Indicates if the user has administrative privileges."
                is_deleted:
                  type: boolean
                  description: "Indicates whether the user account has been marked as deleted."
                is_deleted_at:
                  type: string
                  format: date-time
                  nullable: true
                  description: "Timestamp when the user account was marked as deleted."
                last_activity_at:
                  type: string
                  format: date-time
                  description: "Timestamp of the user's last activity."
                created_at:
                  type: string
                  format: date-time
                  description: "Account creation timestamp."
                updated_at:
                  type: string
                  format: date-time
                  description: "Timestamp of the last update to the user profile."
      404:
        description: User not found.
      500:
        description: Error while retrieving user data.
"""

change_password_doc = """
    User password change.
    ---
    tags:
      - User
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            old_password:
              type: string
              description: Old password
            new_password:
              type: string
              description: New password
            confirm_new_password:
              type: string
              description: Confirmation of the new password
    responses:
      200:
        description: Password updated successfully
      400:
        description: Old password incorrect or missing data
      500:
        description: Server error
"""

delete_my_account_doc = """
    Delete user account.
    ---
    tags:
      - User
    responses:
      200:
        description: User account deleted successfully
      404:
        description: User not found
      500:
        description: Server error
"""

get_all_users_doc = """
    Retrieve all users with pagination (normally admin action but made available to all users here).

    The `online_code` field indicates the user's connection status:
    
    - `0`: user **not connected**
    - `1`: user **connected and online** (active)
    - `2`: user **connected but offline** (inactive beyond 5 minutes)

    The `has_conversation_with` field indicates whether the authenticated user has an active conversation with this user in the list.

    ---
    tags:
      - User
    parameters:
      - name: page
        in: query
        required: false
        type: integer
        default: 1
        description: Page number
      - name: per_page
        in: query
        required: false
        type: integer
        default: 10
        description: Number of users per page
      - name: sort_field
        in: query
        required: false
        type: string
        description: Field to sort by
      - name: sort_direction
        in: query
        required: false
        type: string
        description: Sorting direction (asc or desc)
      - name: filter_field
        in: query
        required: false
        type: string
        enum: [role, is_verified, is_active, is_connected, is_deleted, gender]
        description: Field name to filter by
      - name: filter_value
        in: query
        required: false
        type: string
        description: Value to filter the field with
      - name: q
        in: query
        required: false
        type: string
        description: General search term
      - name: q_name
        in: query
        required: false
        type: string
        description: Search by user name
      - name: q_email
        in: query
        required: false
        type: string
        description: Search by user email
      - name: q_name
        in: query
        required: false
        type: string
        description: Simultaneous search by user firstname and lastname
      - name: q_username
        in: query
        required: false
        type: string
        description: Search by user username
    responses:
      200:
        description: User list retrieved successfully
        schema:
          type: object
          properties:
            users:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  firstname:
                    type: string
                  lastname:
                    type: string
                  email:
                    type: string
                  notifications_count:
                    type: integer
                  is_password_set:
                    type: boolean
                  is_google_authenticated:
                    type: boolean
                  is_admin:
                    type: boolean
                  is_deleted:
                    type: boolean
                  is_verified:
                    type: boolean
                  notifications_count:
                    type: integer
                  is_password_set:
                    type: boolean
                  is_google_authenticated:
                    type: boolean
                  online_code:
                    type: integer
                    enum: [0, 1, 2]
                  has_conversation_with:
                    type: boolean
                  gender:
                    type: string
                  created_at:
                    type: string
                    format: date-time
                  updated_at:
                    type: string
                    format: date-time
            page:
              type: integer
            per_page:
              type: integer
            sort_direction:
              type: string
            q:
              type: string
            has_next:
              type: boolean
            has_prev:
              type: boolean
            total_pages:
              type: integer
            total:
              type: integer
      500:
        description: Server error while retrieving users
        schema:
          id: 500ErrorResponse
          type: object
          properties:
            message:
              type: string
              description: Error message 
            error:
              type: string
              description: Error details
            success:
              type: boolean
              default: false
              description: Indicates if the request was successful or not
"""

get_trashed_users_doc = """
    Retrieve trashed users with pagination (admin action).
    ---
    tags:
      - Administration
    parameters:
      - name: page
        in: query
        required: false
        type: integer
        default: 1
        description: Page number
      - name: per_page
        in: query
        required: false
        type: integer
        default: 10
        description: Number of users per page
      - name: sort_field
        in: query
        required: false
        type: string
        description: Field to sort by
      - name: sort_direction
        in: query
        required: false
        type: string
        description: Sorting direction (asc or desc)
      - name: filter_field
        in: query
        required: false
        type: string
        description: Field name to filter by
      - name: filter_value
        in: query
        required: false
        type: string
        description: Value to filter the field with
      - name: q
        in: query
        required: false
        type: string
        description: General search term
      - name: q_name
        in: query
        required: false
        type: string
        description: Search by user name
      - name: q_email
        in: query
        required: false
        type: string
        description: Search by user email
    responses:
      200:
        description: User list retrieved successfully
        schema:
          type: object
          properties:
            users:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  firstname:
                    type: string
                  lastname:
                    type: string
                  email:
                    type: string
                  is_admin:
                    type: boolean
                  is_deleted:
                    type: boolean
                  is_verified:
                    type: boolean
                  gender:
                    type: string
                  notifications_count:
                    type: integer
                  is_password_set:
                    type: boolean
                  is_google_authenticated:
                    type: string
                  created_at:
                    type: string
                    format: date-time
                  updated_at:
                    type: string
                    format: date-time
            page:
              type: integer
            per_page:
              type: integer
            sort_direction:
              type: string
            q:
              type: string
            has_next:
              type: boolean
            has_prev:
              type: boolean
            total_pages:
              type: integer
            total:
              type: integer
      500:
        description: Server error while retrieving users
        schema:
          id: 500ErrorResponse
          type: object
          properties:
            message:
              type: string
              description: Error message 
            error:
              type: string
              description: Error details
            success:
              type: boolean
              default: false
              description: Indicates if the request was successful or not
"""

user_acount_active_or_not_doc = """
    Activate or deactivate a user account.
    ---
    tags:
      - Administration
    parameters:
      - name: user_id
        in: path
        required: true
        description: Unique user identifier
    responses:
      200:
        description: Account activation status modified successfully
        schema:
          $ref: "#/definitions/200SuccessShortResponse"
      404:
        description: User not found
        schema:
          id: 4xxErrorResponse
          type: object
          properties:
            message:
              type: string
              description: Error message 
            success:
              type: boolean
              default: false
      500:
        description: Server error during activation status modification
        schema:
          $ref: "#/definitions/500ErrorResponse"
"""

user_avatar_doc = """
    Upload or update the connected user's avatar.
    ---
    tags:
      - User
    parameters:
      - name: avatar
        in: formData
        type: file
        required: true
        description: Avatar image file (JPEG, PNG, etc.)
    responses:
      201:
        description: Avatar created or updated successfully
        schema:
          $ref: "#/definitions/User"
      400:
        description: No file provided or invalid request
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      500:
        description: Server error during processing
        schema:
          $ref: "#/definitions/500ErrorResponse"
"""

delete_avatar_doc = """
    Delete the connected user's avatar.
    ---
    tags:
      - User
    responses:
      200:
        description: Avatar deleted successfully
        schema:
          $ref: "#/definitions/200SuccessShortResponse"
      400:
        description: No avatar to delete
      404:
        description: User not found
      500:
        description: Server error during deletion
"""

get_one_user_doc = """
    Retrieve one user's data.
    ---
    tags:
      - Administration
    parameters:
      - name: user_id
        in: path
        required: true
        description: ID of the user whose information is to be retrieved
    responses:
      200:
        description: User data retrieved successfully.
        schema:
          $ref: "#/definitions/User"
      404:
        description: User not found.
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      500:
        description: Error while retrieving user data.
        schema:
          $ref: "#/definitions/500ErrorResponse"
"""

delete_user_account_doc = """
    Delete a user
    ---
    tags:
      - Administration
    parameters:
      - name: user_id
        in: path
        required: true
        description: User ID
    responses:
      200:
        description: User deleted successfully.
        schema:
          $ref: "#/definitions/User"
      404:
        description: User not found.
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      500:
        description: Error during user deletion.
        schema:
          $ref: "#/definitions/500ErrorResponse"
"""

restore_user_account_doc = """
    Restore a deleted user account
    ---
    tags:
      - Administration
    parameters:
      - name: user_id
        in: path
        required: true
        description: User ID
    responses:
      200:
        description: Account restored successfully.
        schema:
          $ref: "#/definitions/User"
      404:
        description: User not found.
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      500:
        description: Error during account restoration.
        schema:
          $ref: "#/definitions/500ErrorResponse"
"""
