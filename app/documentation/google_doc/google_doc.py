login_with_code_doc = """
    Login via Google OAuth2 with an authorization code.
    ---
    tags:
      - Google Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: GoogleLoginWithCode
          required:
            - code
          properties:
            code:
              type: string
              description: Authorization code returned by Google after consent
    responses:
      200:
        description: Successful login with JWT creation
        schema:
          type: object
          properties:
            access_token:
              type: string
              description: JWT token for authenticated requests
      422:
        description: Validation error - The code field is required
      400:
        description: User account deleted or issue with Google email
      500:
        description: Server error during Google login
"""

login_with_refresh_token_doc = """
    Login via Google OAuth2 with a refresh token.
    ---
    tags:
      - Google Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: GoogleLoginWithRefreshToken
          required:
            - refresh_token
          properties:
            refresh_token:
              type: string
              description: Google refresh token allowing regeneration of an access token
    responses:
      200:
        description: Successful login with JWT creation
        schema:
          type: object
          properties:
            access_token:
              type: string
              description: JWT token for authenticated requests
      422:
        description: Validation error - The refresh_token field is required
      400:
        description: User account deleted or issue with Google email
      500:
        description: Server error during Google login
"""

login_with_id_token_doc = """
    Login via Google OAuth2 with an ID token.
    ---
    tags:
      - Google Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: GoogleLoginWithIdToken
          required:
            - id_token
          properties:
            id_token:
              type: string
              description: Google ID token returned after user authentication
    responses:
      200:
        description: Successful login with JWT creation
        schema:
          type: object
          properties:
            access_token:
              type: string
              description: JWT token for authenticated requests
      422:
        description: Validation error - The id_token field is required
      400:
        description: Invalid ID token or issue with authentication information
      500:
        description: Server error during Google login
"""

set_password_doc = """
    Set a user's password.
    This route allows users authenticated via Google on the application to set their password.
    
    It is reserved for users who have not yet set a password on the application (those with the `is_password_set` field set to `False`).
    ---
    tags:
      - Google Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: SetPassword
          required:
            - email
            - new_password
            - confirm_new_password
          properties:
            email:
              type: string
              format: email
              description: User's email address
            new_password:
              type: string
              format: password
              description: Desired new password. It must contain at least 6 characters, an uppercase, a lowercase, a digit, and a special character.
            confirm_new_password:
              type: string
              format: password
              description: Confirmation of the new password. It must be identical to "new_password".
    responses:
      200:
        description: Password set successfully
      422:
        description: Validation error - Required fields missing
      400:
        description: New password and confirmation do not match
      404:
        description: No user found with the provided email
      500:
        description: Server error during password setting
"""
