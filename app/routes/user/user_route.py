
from flask import Blueprint
from flask_jwt_extended import jwt_required
from documentation.user_doc.user_doc import *
from commons.utils.decorators import swagger_doc
from controllers.user.user_controller  import UserController
from commons.utils.admin_user_required import admin_user_required
from commons.utils.valid_user_required import valid_user_required
from commons.utils.none_admin_required import none_admin_required
from commons.utils.update_user_activity import update_user_activity


user = Blueprint('user', __name__,)

@user.route('/admin/add', methods=['POST'])
@swagger_doc(add_admin_doc)
@jwt_required()
@admin_user_required()
@update_user_activity()
def add_admin_route():
    return UserController.add_admin()

@user.route('/profile', methods=['GET'])
@jwt_required()
@valid_user_required()
@update_user_activity()
@swagger_doc(get_user_profile_doc)
def me_route():
    return UserController.get_user_profile()

@user.route('/profile/update', methods=['PUT'])
@jwt_required()
@valid_user_required()
@update_user_activity()
@swagger_doc(update_user_doc)
def update_profile_route():
    return UserController.update_user()

@user.route('/password/update', methods=['PUT'])
@swagger_doc(change_password_doc)
@jwt_required()
@valid_user_required()
@update_user_activity()
def change_password_route():
    return UserController.change_password()

@user.route('/account/delete', methods=['DELETE'])
@jwt_required()
@valid_user_required()
@update_user_activity()
@swagger_doc(delete_my_account_doc)
def delete_my_account_route():
    return UserController. delete_my_account()

@user.route('/avatar/define', methods=['POST'])
@jwt_required()
@valid_user_required()
@update_user_activity()
@swagger_doc(user_avatar_doc)
def create_avatar_route():
    return UserController.user_avatar()

@user.route('/avatar/delete', methods=['DELETE'])
@jwt_required()
@valid_user_required()
@update_user_activity()
@swagger_doc(delete_avatar_doc)
def delete_avatar_route():
    return UserController.delete_avatar()

@user.route('/all', methods=['GET'])
@jwt_required()
@valid_user_required()
@update_user_activity()
@swagger_doc(get_all_users_doc)
def get_all_users_route():
    return UserController.get_all_users()

@user.route('/trashed', methods=['GET'])
@jwt_required()
@admin_user_required()
@update_user_activity()
@swagger_doc(get_trashed_users_doc)
def get_trashed_users_route():
    return UserController.get_all_users(only_deleted=True)

@user.route('/<string:user_id>/get', methods=['GET'])
@jwt_required()
@admin_user_required()
@update_user_activity()
@swagger_doc(get_one_user_doc)
def get_one_user_route(user_id):
    return UserController.get_one_user(user_id)

@user.route('/<string:user_id>/de-or-activate', methods=['PUT'])
@jwt_required()
@admin_user_required()
@update_user_activity()
@swagger_doc(user_acount_active_or_not_doc)
def update_user_active_status(user_id):
    return UserController.toggle_user_active_status(user_id)

@user.route('/<string:user_id>/delete', methods=['DELETE'])
@jwt_required()
@admin_user_required()
@update_user_activity()
@swagger_doc(delete_user_account_doc)
def delete_user_account_route(user_id):
    return UserController.delete_user_account(user_id)

@user.route('/<string:user_id>/restore', methods=['PUT'])
@jwt_required()
@admin_user_required()
@update_user_activity()
@swagger_doc(restore_user_account_doc)
def restore_user_account_route(user_id):
    return UserController.restore_user_account(user_id)
