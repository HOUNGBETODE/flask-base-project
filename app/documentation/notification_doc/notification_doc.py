get_unread_notifications_doc = """
    Retrieve unread notifications for the authenticated user with pagination.
    ---
    tags:
      - Notifications
    parameters:
      - name: page
        in: query
        required: false
        type: integer
        default: 1
        description: "Page number."
      - name: per_page
        in: query
        required: false
        type: integer
        default: 10
        description: "Number of items per page."
    responses:
      200:
        description: Unread notifications retrieved successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              description: "Success message."
            status_code:
              type: integer
              description: "HTTP status code."
            success:
              type: boolean
            data:
              type: object
              properties:
                notifications_data:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      title:
                        type: string
                      message:
                        type: string
                      created_at:
                        type: string
                        format: date-time
                      updated_at:
                        type: string
                        format: date-time
                current_page:
                  type: integer
                page:
                  type: integer
                per_page:
                  type: integer
                total:
                  type: integer
                total_pages:
                  type: integer
                has_next:
                  type: boolean
                has_prev:
                  type: boolean
      500:
        description: Server error when retrieving notifications.
        schema:
          $ref: "#/definitions/500ErrorResponse"
"""

mark_notifications_as_read_doc = """
    Mark unread notifications as read for the authenticated user.

    This endpoint allows marking one or more notifications as read based on the value of the `target` field:

    - If `target` is a **string** equal to `"all"`, then all unread notifications
      of the authenticated user will be marked as read.

    - If `target` is an **integer** (numeric ID), then only the notification corresponding to that ID
      will be marked as read.

    **Examples:**

    - { "target": "all" }   # marks all notifications as read
    - { "target": 42 }      # marks only the notification with ID 42 as read

    ---
    tags:
      - Notifications
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - target
          properties:
            target:
              type: string
              description: "Target to mark as read, can be 'all' or a specific notification ID."
    responses:
      200:
        description: Notifications marked as read successfully.
        schema:
          $ref: "#/definitions/200SuccessShortResponse"
      400:
        description: The 'target' field is required or invalid.
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      500:
        description: Server error when updating notifications.
        schema:
          $ref: "#/definitions/500ErrorResponse"
"""
