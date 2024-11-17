from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, Home
from forms import CompanyDetailsForm, SocialsForm
from . import dashboard_bp
from utils.decorators import roles_required
from forms import HomePageContentForm


@dashboard_bp.app_context_processor
def inject_home_content_status():
    home_exists = Home.query.count() > 0
    return {'home_exists': home_exists}



@dashboard_bp.route('/add-home-content', methods=['GET', 'POST'])
@roles_required('Admin')
def add_home_content():
    """
    This function adds a home page content to the database
    """
    form = HomePageContentForm()
    if form.validate_on_submit():
        try:
            # Create a new instance of Home and add it to the database
            new_home_content = Home(
                heading=form.heading.data,
                subheading=form.subheading.data,
                description=form.description.data,
                image_one= form.image_one.data,
                image_two= form.image_two.data,
                image_three= form.image_three.data,
                image_four= form.image_four.data
            )
            db.session.add(new_home_content)
            db.session.commit()
            flash('Home Page Content added successfully', 'success')
            return redirect(url_for('dashboard_bp.update_home_page'))
        except Exception as e:
            # If something goes wrong, roll back and print the error
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    else:
        # Log if form validation fails
        print("Form validation failed. Errors:", form.errors)
        flash('Please correct the errors in the form', 'danger')

    return render_template('dashboard/home/add-home-content.html', form=form)



@dashboard_bp.route('/update-Home-Page', methods=['GET', 'POST'])
@roles_required('Admin')
def update_home_page():
    """
    This function updates the home page content
    """
    # Retrieve the first item from the Home table
    home_content_to_update = Home.query.first()
    if not home_content_to_update:
        flash("No home content found to update, Please add the content below.", 'warning')
        return redirect(url_for('dashboard_bp.add_home_content'))

    form = HomePageContentForm()

    # Pre-populate the form with existing data for GET requests
    if request.method == 'GET':
        form.subheading.data = home_content_to_update.subheading
        form.description.data = home_content_to_update.description
        form.img_url.data = home_content_to_update.img_url

    if form.validate_on_submit():
        # Assign updated values to the home_content_to_update instance
        home_content_to_update.subheading = form.subheading.data
        home_content_to_update.description = form.description.data
        home_content_to_update.img_url = form.img_url.data

        db.session.commit()
        flash('Home Page Content updated successfully.', 'success')
        return redirect(url_for('dashboard_bp.update_home_page'))

    return render_template('dashboard/home/update-home-content.html', form=form, home=home_content_to_update)