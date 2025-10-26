class ResponseData:

    @staticmethod
    def login(access_token):
        """
        Structure les données de la réponse pour la connexion d'un utilisateur.
        """
        return {
            'access_token': access_token
        }


    @staticmethod
    def get_all_users(users_data, page, per_page, current_page, sort_direction, sort_field, q, total_pages, total, filter_field, filter_value, q_name, q_email, q_username, has_next, has_prev):
        return{
            'users_data': users_data,
            'page': page,
            'per_page': per_page,
            "current_page": current_page,
            'sort_direction': sort_direction,
            'sort_field': sort_field,
            'q': q,
            'total_pages': total_pages,
            'total': total,
            'filter_field': filter_field,
            'filter_value': filter_value,
            'q_name': q_name,
            'q_email': q_email,
            'q_username': q_username,
            'has_next': has_next,
            'has_prev': has_prev
        }


    @staticmethod
    def get_all_activities(activities_data, page, per_page, current_page, sort_direction, sort_field, q, total_pages, total, has_next, has_prev):
        return{
            'activities_data': activities_data,
            'page': page,
            'per_page': per_page,
            "current_page": current_page,
            'sort_direction': sort_direction,
            'sort_field': sort_field,
            'q': q,
            'total_pages': total_pages,
            'total': total,
            'has_next': has_next,
            'has_prev': has_prev
        }
    

    @staticmethod
    def get_all_comments(comments_data, page, per_page, current_page, sort_direction, sort_field, q, total_pages, total, has_next, has_prev):
        return{
            'comments_data': comments_data,
            'page': page,
            'per_page': per_page,
            "current_page": current_page,
            'sort_direction': sort_direction,
            'sort_field': sort_field,
            'q': q,
            'total_pages': total_pages,
            'total': total,
            'has_next': has_next,
            'has_prev': has_prev
        }


    @staticmethod
    def get_all_stands(stands_data, page, per_page, current_page, sort_direction, sort_field, q, q_enterprise, q_city, q_address, q_status, total_pages, total, has_next, has_prev):
        return{
            'stands_data': stands_data,
            'page': page,
            'per_page': per_page,
            "current_page": current_page,
            'sort_direction': sort_direction,
            'sort_field': sort_field,
            'q': q,
            'q_enterprise': q_enterprise,
            'q_city': q_city,
            'q_address': q_address,
            'q_status': q_status,
            'total_pages': total_pages,
            'total': total,
            'has_next': has_next,
            'has_prev': has_prev
        }


    @staticmethod
    def get_all_messages(other_user_data, messages_data, page, per_page, current_page, total_pages, total, has_next, has_prev):
        return{
            'other_user_data': other_user_data,
            'messages_data': messages_data,
            'page': page,
            'per_page': per_page,
            "current_page": current_page,
            'total_pages': total_pages,
            'total': total,
            'has_next': has_next,
            'has_prev': has_prev
        }
    

    @staticmethod
    def get_all_conversations(conversations_data, page, per_page, current_page, total_pages, total, has_next, has_prev):
        return{
            'conversations_data': conversations_data,
            'page': page,
            'per_page': per_page,
            "current_page": current_page,
            'total_pages': total_pages,
            'total': total,
            'has_next': has_next,
            'has_prev': has_prev
        }


    @staticmethod
    def get_all_services(services_data, page, per_page, current_page, sort_direction, sort_field, q, q_title, total_pages, total, has_next, has_prev):
        return{
            'services_data': services_data,
            'page': page,
            'per_page': per_page,
            "current_page": current_page,
            'sort_direction': sort_direction,
            'sort_field': sort_field,
            'q': q,
            'q_title': q_title,
            'total_pages': total_pages,
            'total': total,
            'has_next': has_next,
            'has_prev': has_prev
        }


    @staticmethod
    def get_all_posts(posts_data, page, per_page, current_page, sort_direction, sort_field, q, total_pages, total, has_next, has_prev):
        return{
            'posts_data': posts_data,
            'page': page,
            'per_page': per_page,
            "current_page": current_page,
            'sort_direction': sort_direction,
            'sort_field': sort_field,
            'q': q,
            'total_pages': total_pages,
            'total': total,
            'has_next': has_next,
            'has_prev': has_prev
        }


    @staticmethod
    def get_all_notifications(notifications_data, page, per_page, current_page, total_pages, total, has_next, has_prev):
        return{
            'notifications_data': notifications_data,
            'page': page,
            'per_page': per_page,
            "current_page": current_page,
            'total_pages': total_pages,
            'total': total,
            'has_next': has_next,
            'has_prev': has_prev
        }


    @staticmethod
    def get_all_orders(orders_data, page, per_page, current_page, sort_direction, sort_field, q, total_pages, total, filter_field, filter_value, has_next, has_prev, order_summary = None, income_summary = None):
        response_base_dict = {
            'orders_data': orders_data,
            'page': page,
            'per_page': per_page,
            "current_page": current_page,
            'sort_direction': sort_direction,
            'sort_field': sort_field,
            'q': q,
            'total_pages': total_pages,
            'total': total,
            'filter_field': filter_field,
            'filter_value': filter_value,
            'has_next': has_next,
            'has_prev': has_prev
        }

        if income_summary and order_summary:
            response_base_dict.update({
                "order_summary": order_summary,
                "income_summary": income_summary
            })
        
        return response_base_dict
