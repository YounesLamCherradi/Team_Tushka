# HOME PAGE ROUTE
@app.route('/welcome')
def welcome():
    return render_template('home.html')

# SIGNUP PAGE ROUTE
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        alumni = 'alumni' in request.form  # Checks if the alumni checkbox is selected

        # Check if the email is already registered
        user_exists = collection.find_one({'email': email})
        if user_exists:
            flash('Email already exists.', 'danger')
            return render_template('signup.html')

        # Create a new user with the role of "user"
        new_user = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,  # In production, hash the password before storing
            'alumni': alumni,
            'role': 'user'  # Set role to "user" by default
        }
        
        # Insert new user into the database
        result = collection.insert_one(new_user)
        
        # Set session variables for the newly signed up user
        session['user_id'] = str(result.inserted_id)  # Get the ID of the newly inserted user
        session['email'] = email
        session['role'] = 'user'  # Set the role as user
        session['logged_in'] = True  # Mark as logged in

        flash('Signup successful! You are now logged in.', 'success')
        # Redirect to the user dashboard after successful signup
        return redirect(url_for('user_dashboard'))
    
    return render_template('signup.html')




# LOGIN PAGE ROUTE
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the user exists in the database
        user = collection.find_one({'email': email, 'password': password})

        if user:
            # Store user information in session for logged-in status
            session['user_id'] = str(user['_id'])  # User ID
            session['email'] = user['email']  # User email
            session['role'] = user.get('role', 'user')  # User role; default to 'user'
            session['logged_in'] = True  # Set logged-in status

            flash('Logged in successfully!', 'success')

            # Redirect based on user role
            if session['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))  # For regular users
        else:
            flash('Invalid email or password.', 'danger')
            return render_template('login.html')

    return render_template('login.html')


