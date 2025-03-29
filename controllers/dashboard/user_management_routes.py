from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_required
from utils.decorators import roles_required
from utils.decorators import  nocache
from datetime import date
from utils.email_utils import send_approval_message, send_demotion_message
from . import dashboard_bp
from models import db, User, Home
from utils.encryption import check_password_hash, generate_password_hash
from forms import UpdateEmailForm, UpdatePhoneForm, ChangePasswordForm


#TODO:
#TODO: Protect the user management routes with the roles_required decorator
#TODO: make the profile route limited to the current user so that it can only be accessed by the user
#TODO: Modify the templates in templates/admin
# Create wtf forms for user management
# Create the add user function and automatically send them an email with their login details urging them to change their password



@dashboard_bp.route('/get-all-users', methods=['GET'])
@roles_required('Admin')
def get_users():
    """
    This function gets all the users from the database
    :return:
    """
    users = User.query.all()
    return render_template('/admin/user-manager.html', users=users)



# @dashboard_bp.route('/edit-user/<int:user_id>', methods=['GET','POST'])
# @roles_required('Admin')
# def manage_user(user_id):
#     user = User.query.get_or_404(user_id)
#
#     form = ChangeUserRoleForm()
#     if request.method == 'POST':
#         new_role = request.form.get('new_role')
#         if new_role in ['User', 'Contributor']:
#             if user.role == new_role:
#                 flash(f"No Changes made because {user.first_name} is already a {new_role}.", 'info')
#             else:
#                 user.role = new_role
#
#                 if new_role == 'Contributor':
#                     send_approval_message(name=user.first_name, email=user.email, subject='Contributor Approval for')
#                     db.session.commit()
#                     flash(f"{user.first_name}'s role has been updated to {new_role}.", 'success')
#
#                 else:
#                     db.session.commit()
#                     send_demotion_message(name=user.first_name, email=user.email, subject='Current Role Update')
#                     flash(f"{user.first_name}'s role has been updated to {new_role}.", 'success')
#
#         else:
#             flash('Invalid role selected.', 'danger')
#         return redirect(url_for('dashboard_bp.manage_user', user_id=user.id))
#     return render_template('admin/edit-user.html', user=user, form=form)


# @dashboard_bp.route('/add-user', methods=['GET', 'POST'])
# @roles_required('Admin')
# def add_user():
#     """
#     This function adds a new user to the database
#     :return:
#     """
#     form = AddUserForm()
#     if form.validate_on_submit():
#         email = form.email.data
#         first_name = form.first_name.data
#         last_name = form.last_name.data
#         password = form.password.data
#         role = form.role.data
#         user = User.query.filter_by(email=email).first()
#         if user:
#             flash(f"{email} already exists in the database.", 'danger')
#             return redirect(url_for('dashboard_bp.add_user'))
#         else:
#             hashed_password = hash_and_salt_password(password)
#             new_user = User(
#                 email=email,
#                 first_name=first_name,
#                 last_name=last_name,
#                 password=hashed_password,
#                 role=role
#             )
#             db.session.add(new_user)
#             db.session.commit()
#             flash(f"{first_name} {last_name} has been added successfully.", 'success')
#             return redirect(url_for('dashboard_bp.get_users'))
#     return render_template('admin/add-user.html', form=form)

# @dashboard_bp.route('/blacklist-user/<int:user_id>', methods=['GET', 'POST'])
# @roles_required('Admin')
# def blacklist_user(user_id):
#     """
#     This function blacklists a user
#     :param user_id:
#     :return
#     """
#     user = User.query.get_or_404(user_id)
#     user.is_blacklisted = True
#     db.session.commit()
#     flash(f"{user.first_name} has been blacklisted.", 'success')
#     return redirect(url_for('dashboard_bp.get_users'))
#
#
#
# @dashboard_bp.route('/unblacklist-user/<int:user_id>', methods=['GET', 'POST'])
# @roles_required('Admin')
# def unblacklist_user(user_id):
#     """
#     This function unblacklists a user
#     :param user_id:
#     :return
#     """
#     user = User.query.get_or_404(user_id)
#     user.is_blacklisted = False
#     db.session.commit()
#     flash(f"{user.first_name} has been unblacklisted.", 'success')
#     return redirect(url_for('dashboard_bp.get_users'))
#
# #TODO add blacklist user
# @dashboard_bp.route('/delete-user/<int:user_id>', methods=['GET', 'DELETE'])
# @roles_required('Admin')
# def delete_user(user_id):
#     """
#     This function deletes a user from the database
#     :param user_id:
#     :return:
#     """
#     user_to_delete = User.query.get_or_404(user_id)
#     db.session.delete(user_to_delete)
#     db.session.commit()
#     flash('User deleted successfully', 'success')
#     return redirect(url_for('dashboard_bp.get_users'))