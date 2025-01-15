from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Jobs_Done, Reviewer
from . import dashboard_bp
from utils.file_upload_helper import save_file
from forms import JobsDoneForm, ReviewerForm
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads/jobs_done'

@dashboard_bp.route('/jobs-done', methods=['GET'])
@login_required
def list_jobs_done():
    jobs = Jobs_Done.query.all()
    return render_template('dashboard/jobs_done/jobs_done.html', jobs=jobs)

@dashboard_bp.route('/add-job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobsDoneForm()
    if form.validate_on_submit():
        main_image = form.main_image_path.data

        # Save images to 'static/uploads/jobs_done'
        main_image_path = save_file(form.main_image_path.data,
                                    subfolder='jobs_done') if form.main_image_path.data else None


        new_job = Jobs_Done(
            name=form.name.data,
            image=main_image_path,
            location=form.location.data,
            service_provider_id=current_user.id
        )

        db.session.add(new_job)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('dashboard_bp.list_jobs_done'))

    return render_template('dashboard/jobs_done/add_job.html', form=form)



@dashboard_bp.route('/edit-job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    """
    Edit an existing Jobs_Done entry.
    """
    job_to_update= Jobs_Done.query.get_or_404(job_id)
    form = JobsDoneForm(obj=job_to_update)  # Pre-populate with existing data

    if form.validate_on_submit():
        # Handle file uploads and delete old files if a new file is uploaded

            # Handle file uploads and remove old files if a new file is uploaded
        if form.main_image_path.data and hasattr(form.main_image_path.data, 'filename'):
            old_main_image = job_to_update.image
            job_to_update.image = save_file(form.main_image_path.data, subfolder='jobs_done')
            if old_main_image:
                old_full_path = old_main_image.lstrip('/')
                if os.path.exists(old_full_path):
                    os.remove(old_full_path)



        # Update text fields
        job_to_update.name = form.name.data
        job_to_update.location = form.location.data

        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('dashboard_bp.list_jobs_done'))

    return render_template('dashboard/jobs_done/edit_job.html', form=form, job=job_to_update)


@dashboard_bp.route('/delete-job/<int:job_id>', methods=['DELETE', 'GET'])
@login_required
def delete_job(job_id):
    """
    Delete a Jobs_Done entry and its associated files.
    """
    job_to_delete = Jobs_Done.query.get_or_404(job_id)

    # Remove associated uploaded files
    file_paths = [
        job_to_delete.image,

    ]

    for file_path in file_paths:
        if file_path:
            # Convert '/static/...path...' to 'static/...path...'
            old_full_path = file_path.lstrip('/')
            if os.path.exists(old_full_path):
                os.remove(old_full_path)

    # Delete the project from the database
    db.session.delete(job_to_delete)
    db.session.commit()
    flash(f'Project: {job_to_delete.name}  deleted successfully!', 'info')
    return redirect(url_for('dashboard_bp.list_jobs_done'))

@dashboard_bp.route('/add-review/<int:job_id>', methods=['GET', 'POST'])
def add_review(job_id):
    form = ReviewerForm()
    job = Jobs_Done.query.get_or_404(job_id)
    if form.validate_on_submit():
        review = Reviewer(
            name=form.name.data,
            review=form.review.data,
            job_id=job_id
        )
        db.session.add(review)
        db.session.commit()
        flash('Review added successfully!', 'success')
        return redirect(url_for('dashboard_bp.view_job', job_id=job.id))
    return render_template('dashboard/jobs_done/add_review.html', form=form, job=job)
