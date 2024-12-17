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
        before_image = form.image_one_path.data
        after_image = form.image_two_path.data

        # Save images to 'static/uploads/jobs_done'
        main_image_path = save_file(main_image, subfolder='jobs_done') if main_image else None
        image_one_path = save_file(before_image, subfolder='jobs_done') if before_image else None
        image_two_path = save_file(after_image, subfolder='jobs_done') if after_image else None

        new_job = Jobs_Done(
            name=form.name.data,
            main_image_path=main_image_path,
            image_one_path=image_one_path,
            image_two_path=image_two_path,
            description=form.description.data,
            location=form.location.data,
            User_id=current_user.id
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
    job = Jobs_Done.query.get_or_404(job_id)
    form = JobsDoneForm(obj=job)  # Pre-populate with existing data

    if form.validate_on_submit():
        # Handle file uploads and delete old files if a new file is uploaded
        if form.main_image_path.data:
            if job.main_image_path:
                old_full_path = job.main_image_path.lstrip('/')  # Convert '/static/...' to 'static/...'
                if os.path.exists(old_full_path):
                    os.remove(old_full_path)
            job.main_image_path = save_file(form.main_image_path.data, subfolder='jobs_done')

        if form.image_one_path.data:
            if job.image_one_path:
                old_full_path = job.image_one_path.lstrip('/')
                if os.path.exists(old_full_path):
                    os.remove(old_full_path)
            job.image_one_path = save_file(form.image_one_path.data, subfolder='jobs_done')

        if form.image_two_path.data:
            if job.image_two_path:
                old_full_path = job.image_two_path.lstrip('/')
                if os.path.exists(old_full_path):
                    os.remove(old_full_path)
            job.image_two_path = save_file(form.image_two_path.data, subfolder='jobs_done')

        # Update text fields
        job.name = form.name.data
        job.description = form.description.data
        job.location = form.location.data

        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('dashboard_bp.list_jobs_done'))

    return render_template('dashboard/jobs_done/edit_job.html', form=form, job=job)


@dashboard_bp.route('/delete-job/<int:job_id>', methods=['DELETE', 'GET'])
@login_required
def delete_job(job_id):
    """
    Delete a Jobs_Done entry and its associated files.
    """
    job = Jobs_Done.query.get_or_404(job_id)

    # Remove associated uploaded files
    file_paths = [
        job.main_image_path,
        job.image_one_path,
        job.image_two_path,
    ]

    for file_path in file_paths:
        if file_path:
            old_full_path = file_path.lstrip('/')  # Convert '/static/...' to 'static/...'
            if os.path.exists(old_full_path):
                os.remove(old_full_path)

    # Delete the project from the database
    db.session.delete(job)
    db.session.commit()
    flash('Project deleted successfully!', 'info')
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
