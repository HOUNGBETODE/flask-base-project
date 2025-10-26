signup_doc = """
    Sign up a new user.
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Signup
          required:
            - firstname
            - lastname
            - email
            - username
            - password
            - confirm_password
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
            gender:
              type: string
              enum: [male, female]
              description: User's gender
              default: male
            email:
              type: string
              format: email
              description: User's email address
            password:
              type: string
              format: password
              description: Password for the account. Must comply with defined security rules - contain at least 6 characters including an uppercase, a lowercase, a digit and a special character
            confirm_password:
              type: string
              format: password
              description: Password confirmation. Must be identical to the "password" field
    responses:
      201:
        description: Account created successfully
      400:
        description: This email is already taken
      422:
        description: Validation error - Required fields missing | Passwords do not match | Invalid gender value
      500:
        description: Server error during account creation
"""

login_doc = """
    User login.
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Login
          required:
            - credential
            - password
          properties:
            credential:
              type: string
              description: User's username or email address
            password:
              type: string
              format: password
              description: Account password
    responses:
      200:
        description: Successful login
        schema:
          type: object
          properties:
            access_token:
              type: string
              description: JWT token for authenticated requests
      422:
        description: Validation error - Required fields missing
      400:
        description: Email or password is incorrect
      500:
        description: Server error during login
"""

logout_doc = """
    User logout.
    ---
    tags:
      - Authentication
    responses:
      200:
        description: Successful logout
        schema:
          id: 200SuccessShortResponse
          type: object
          properties:
            message:
              type: string
              description: Success message
            success:
              type: boolean
              default: true
      400:
        description: JWT ID (jti) not found or invalid token
      400:
        description: Error during user logout
      500:
        description: Internal server error or token revocation failure
"""

forgot_password_doc = """
    Request a password reset code.
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              format: email
              description: User's email address
    responses:
      200:
        description: Code sent successfully
      400:
        description: Error sending the code
      422:
        description: Email is required
      500:
        description: Internal server error or failure
"""

reset_password_doc = """
    Reset password using a code.
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              format: email
              description: User's email address
            otp_code:
              type: number
              description: Reset code sent by email
            new_password:
              type: string
              description: New password
            confirm_new_password:
              type: string
              description: Confirmation of new password
    responses:
      200:
        description: Password successfully updated
      400:
        description: Invalid reset code or missing data
      500:
        description: Server error
"""

verify_user_doc = """
    User account verification via a code sent by email.
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              format: email
              description: User's email address
            otp_code:
              type: number
              description: Verification code received via email
    responses:
      200:
        description: Account successfully verified
      400:
        description: Incorrect verification code or missing data
      404:
        description: User not found
      500:
        description: Server error
"""

user_verify_resent_code = """
    Resend user account verification code.
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              format: email
              description: User's email address
    responses:
      200:
        description: Verification code successfully sent
      400:
        description: Email not provided or missing data
      404:
        description: User not found or account already verified
      500:
        description: Server error
"""
