@app.route('/create-position', methods=['POST'])
def create_position():
    if 'user_id' in session and session.get('role') == 'admin':
        title = request.form.get('title')
        location = request.form.get('location')
        description = request.form.get('description')

        new_post = {
            'title': title,
            'location': location,
            'description': description
        }
        posts_collection.insert_one(new_post)
        flash('Position created successfully!', 'success')
        return redirect(url_for('manage_vacancies'))
    else:
        flash("You do not have access to this page.", "warning")
        return redirect(url_for('login'))

# EDIT POSITION ROUTE
@app.route('/edit-position/<post_id>', methods=['GET', 'POST'])
def edit_position(post_id):
    if 'user_id' in session and session.get('role') == 'admin':
        post = posts_collection.find_one({'_id': ObjectId(post_id)})
        if request.method == 'POST':
            updated_title = request.form.get('title')
            updated_location = request.form.get('location')
            updated_description = request.form.get('description')

            posts_collection.update_one(
                {'_id': ObjectId(post_id)},
                {'$set': {
                    'title': updated_title,
                    'location': updated_location,
                    'description': updated_description
                }}
            )
            flash('Position updated successfully!', 'success')
            return redirect(url_for('manage_vacancies'))
        
        return render_template('admin_edit_position.html', post=post)  # Ensure 'post' is passed here
    else:
        flash("You do not have access to this page.", "warning")
        return redirect(url_for('login'))

# DELETE POSITION ROUTE
@app.route('/delete-position/<post_id>', methods=['POST'])
def delete_position(post_id):
    if 'user_id' in session and session.get('role') == 'admin':
        posts_collection.delete_one({'_id': ObjectId(post_id)})
        flash('Position deleted successfully!', 'success')
        return redirect(url_for('manage_vacancies'))
    else:
        flash("You do not have access to this page.", "warning")
        return redirect(url_for('login'))


# USER MANAGEMENT ROUTE
@app.route('/user-management')
def user_management():
    # Ensure only admins can access this route
    if 'user_id' in session and session.get('role') == 'admin':
        users = list(collection.find())
        return render_template('admin_user_management.html', users=users)
    else:
        flash("You do not have access to this page.", "warning")
        return redirect(url_for('login'))

# ADD USER ROUTE
@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if 'user_id' in session and session.get('role') == 'admin':
        if request.method == 'POST':
            # Collect user details from the form
            username = request.form.get('username')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role')  # Role can be 'user' or 'admin'

            # Check if the email is already registered
            user_exists = collection.find_one({'email': email})
            if user_exists:
                flash('Email already exists.', 'danger')
                return redirect(url_for('add_user'))

            # Insert new user into the database
            new_user = {
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password,  # Hash password in production
                'role': role
            }
            collection.insert_one(new_user)
            flash('User added successfully!', 'success')
            return redirect(url_for('user_management'))

        return render_template('admin_add_user.html')
    else:
        flash("You do not have access to this page.", "warning")
        return redirect(url_for('login'))