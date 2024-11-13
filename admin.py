# ADMIN DASHBOARD ROUTE
@app.route('/admin-dashboard')
def admin_dashboard():
    if 'user_id' in session and session.get('role') == 'admin':
        return render_template('admin_dashboard.html', admin_name=session['email'])
    else:
        flash("You do not have access to this page.", "warning")
        return redirect(url_for('login'))
    
# Route to display all applications
@app.route('/check-applications')
def check_applications():
    if 'user_id' in session and session.get('role') == 'admin':
        # Retrieve applications from the database
        applications = list(applications_collection.find())
        return render_template('check_application.html', applications=applications, admin_name=session.get('email'))
    else:
        flash("You do not have access to this page.", "warning")
        return redirect(url_for('login'))

# Route to view application details
@app.route('/application-details/<application_id>')
def application_details(application_id):
    if 'user_id' in session and session.get('role') == 'admin':
        # Fetch specific application from the database
        application = applications_collection.find_one({'_id': ObjectId(application_id)})
        if not application:
            flash("Application not found.", "danger")
            return redirect(url_for('check_applications'))

        # Optionally fetch related position data if needed
        position = posts_collection.find_one({'_id': ObjectId(application['position_id'])}) if 'position_id' in application else None
        return render_template('application_details.html', application=application, position=position)
    else:
        flash("You do not have access to this page.", "warning")
        return redirect(url_for('login'))

@app.route('/manage-vacancies')
def manage_vacancies():
    if 'user_id' in session and session.get('role') == 'admin':
        vacancies = list(posts_collection.find())  # Change variable name to 'vacancies' for consistency
        return render_template('admin_manage_vacancies.html', vacancies=vacancies)  # Pass 'vacancies' to match the HTML
    else:
        flash("You do not have access to this page.", "warning")
        return redirect(url_for('login'))
    