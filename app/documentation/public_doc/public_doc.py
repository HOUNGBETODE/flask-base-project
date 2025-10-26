public_controller_doc = {
    "find_username": """
    Check the availability of a username.
    ---
    parameters:
      - name: username
        in: path
        required: true
        type: string
        description: Username to check.
    responses:
      200:
        description: Username available.
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Username available.
      400:
        description: Username already taken.
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      422:
        description: Invalid username (too short or incorrect format).
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      500:
        description: Server error.
        schema:
          $ref: "#/definitions/500ErrorResponse"
    """,
}
