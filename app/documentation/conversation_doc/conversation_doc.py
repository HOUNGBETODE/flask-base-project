from commons.const.string.app_string import AppString

conversation_controller_doc = {
    # Documentation for ConversationController.create
    "create": """
    Create a new conversation.
    ---
    tags:
      - Conversation
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            user_id:
              type: string
              description: ID of the user to initiate conversation with.
    responses:
      201:
        description: Conversation successfully created.
        schema:
          type: object
          properties:
            message:
              type: string
            success:
              type: boolean
            data:
              type: object
              properties:
                id:
                  type: string
                  description: Unique identifier of the conversation.
                created_at:
                  type: string
                  format: date-time
                  description: Conversation creation timestamp.
                updated_at:
                  type: string
                  format: date-time
                  description: Conversation last update timestamp.
                is_deleted:
                  type: boolean
                  default: false
                  description: Indicates whether the conversation has been marked as deleted.
                is_deleted_at:
                  type: string
                  format: date-time
                  description: Timestamp when the conversation was deleted.
                messengers:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: string
                        description: Unique identifier of a participant in the conversation.
                      unread_count:
                        type: integer
                        description: Number of unread messages for this participant in the conversation.
      422:
        description: Validation error (missing fields).
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      404:
        description: Stand or user not found.
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      400:
        description: This conversation already exists.
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      500:
        description: Server error.
        schema:
          $ref: "#/definitions/500ErrorResponse"
""",

    # Documentation for ConversationController.get_all_for_user
    "get_all_for_user": """
    Retrieve the conversation history of the authenticated user.
    ---
    tags:
      - Conversation
    parameters:
      - name: page
        in: query
        required: false
        type: integer
        default: 1
        description: Page number.
      - name: per_page
        in: query
        required: false
        type: integer
        default: 10
        description: Number of conversations per page.
    responses:
      200:
        description: Conversation history retrieved successfully.
        schema:
          type: object
          properties:
            message:
              type: string
            success:
              type: boolean
            data:
              type: object
              properties:
                conversations_data:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: string
                      unread_count:
                        type: integer
                      last_message:
                        type: object
                        properties:
                          id:
                            type: integer
                          content:
                            type: string
                          date:
                            type: string
                            format: date-time
                          is_first:
                            type: boolean
                            default: false
                          is_modified:
                            type: boolean
                            default: false
                      other_user:
                        type: object
                        properties:
                          id:
                            type: string
                          email:
                            type: string
                            format: email
                          avatar:
                            type: string
                            format: uri
                          firstname:
                            type: string
                          lastname:
                            type: string
                          username:
                            type: string
                          gender:
                            type: string
                            enum: [male, female]
                          is_active:
                            type: boolean
                          is_deleted:
                            type: boolean
                            default: false
                page:
                  type: integer
                per_page:
                  type: integer
                current_page:
                  type: integer
                total_pages:
                  type: integer
                total:
                  type: integer
                has_next:
                  type: boolean
                has_prev:
                  type: boolean
      500:
        description: Server error.
        schema:
          $ref: "#/definitions/500ErrorResponse"
""",

    # Documentation for MessageController.get_all_messages
    "get_all_messages": """
    Retrieve all messages from a specific conversation.
    ---
    tags:
      - Message
    parameters:
      - name: conversation_id
        in: path
        required: true
        type: string
        description: Unique identifier of the conversation.
      - name: page
        in: query
        required: false
        type: integer
        default: 1
        description: Page number.
      - name: per_page
        in: query
        required: false
        type: integer
        default: 10
        description: Number of messages per page.
    responses:
      200:
        description: Messages successfully retrieved.
        schema:
          type: object
          properties:
            message:
              type: string
            success:
              type: boolean
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  conversation_id:
                    type: integer
                  is_stand_writer:
                    type: boolean
                  content:
                    type: string
                  attachment_count:
                    type: integer
                  attachments:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: integer
                        file_name:
                          type: string
                        file_path:
                          type: string
                          format: uri
                        file_size:
                          type: integer
                  created_at:
                    type: string
                    format: date-time
                  updated_at:
                    type: string
                    format: date-time
      404:
        description: Conversation not found.
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      500:
        description: Server error.
        schema:
          $ref: "#/definitions/500ErrorResponse"
""",

    # Documentation for MessageController.send_message_with_attachments
    "send_message_with_attachments": """
    Send a message with or without attachments.
    ---
    tags:
      - Message
    parameters:
      - name: conversation_id
        in: path
        required: true
        type: string
        description: Unique identifier of the conversation.
      - name: files
        in: formData
        required: false
        type: file
        description: File attachments.
        collectionFormat: multi
      - name: content
        in: formData
        required: false
        type: string
        description: Text content of the message.
    responses:
      201:
        description: Message sent successfully.
        schema:
          $ref: "#/definitions/200SuccessShortResponse"
      400:
        description: Validation error (missing required fields).
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      404:
        description: Conversation not found.
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      403:
        description: Unauthorized to send a message in this conversation.
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      500:
        description: Server error.
        schema:
          $ref: "#/definitions/500ErrorResponse"
""",

    # Documentation for MessageController.update
    "update_message_content": f"""
    Update a message within {AppString.time_limit_for_message}s.
    ---
    tags:
      - Message
    parameters:
      - name: conversation_id
        in: path
        required: true
        type: string
        description: Unique identifier of the conversation.
      - name: message_id
        in: path
        required: true
        type: integer
        description: Unique identifier of the message.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            content:
              type: string
              description: New message content.
    responses:
      200:
        description: Message successfully updated.
        schema:
          type: object
          properties:
            message:
              type: string
            success:
              type: boolean
      404:
        description: Message not found.
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      403:
        description: Unauthorized to update this message.
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      400:
        description: No change detected in the content or the update time window has expired.
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      500:
        description: Server error.
        schema:
          $ref: "#/definitions/500ErrorResponse"
""",

    # Documentation for MessageController.delete
    "delete_message": f"""
    Delete a message within {AppString.time_limit_for_message}s.
    ---
    tags:
      - Message
    parameters:
      - name: conversation_id
        in: path
        required: true
        type: string
        description: Unique identifier of the conversation.
      - name: message_id
        in: path
        required: true
        type: integer
        description: Unique identifier of the message to delete.
    responses:
      200:
        description: Message successfully deleted.
        schema:
          $ref: "#/definitions/200SuccessShortResponse"
      404:
        description: Message or conversation not found.
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      403:
        description: Unauthorized to delete this message.
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      500:
        description: Server error.
        schema:
          $ref: "#/definitions/500ErrorResponse"
""",

    # Documentation for MessageController.attachment_delete
    "attachment_delete": f"""
    Delete an attachment within {AppString.time_limit_for_message}s.
    ---
    tags:
      - Message
    parameters:
      - name: conversation_id
        in: path
        required: true
        type: string
        description: Unique identifier of the conversation.
      - name: attachment_id
        in: path
        required: true
        type: integer
        description: Unique identifier of the attachment to delete.
    responses:
      200:
        description: Attachment successfully deleted.
        schema:
          $ref: "#/definitions/200SuccessShortResponse"
      404:
        description: Attachment or conversation not found.
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      403:
        description: Unauthorized to delete this attachment.
        schema:
          $ref: "#/definitions/4xxErrorResponse"
      500:
        description: Server error.
        schema:
          $ref: "#/definitions/500ErrorResponse"
"""
}
