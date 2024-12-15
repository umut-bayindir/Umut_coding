Compilation : python3 app.py


# Flask Application - Purpose of Functions

### **1. `get_db_connection`**
- **Purpose**: Establishes a connection to the PostgreSQL database using the configured database credentials. 
- **Usage**: This function is called whenever the application needs to interact with the database to execute queries or transactions.

---

### **2. `create_tables`**
- **Purpose**: Creates the necessary database tables (`Roles`, `Department`, `Users`, `Project`, `Employee`) when the application is initialized. It ensures that all required tables exist before the application starts handling requests.
- **Key Points**:
  - Uses SQL `CREATE TABLE` statements with foreign key relationships for data integrity.
  - Prevents duplicate table creation with the `IF NOT EXISTS` clause.

---

### **3. `populate_tables`**
- **Purpose**: Populates the `Roles` and `Department` tables with initial data required for the application to function. 
- **Usage**: Typically used during setup or testing to ensure that the application starts with predefined roles and departments.
- **Key Points**:
  - Inserts roles like "admin", "department_head", and "employee".
  - Adds example departments such as "Computing" and "Plumbing".

---

### **4. `home`**
- **Purpose**: Serves the homepage of the application.
- **Functionality**:
  - If a user is logged in, fetches their username from the database and displays it on the homepage.
  - Renders the `index.html` template.

---

### **5. `login`**
- **Purpose**: Handles user authentication.
- **Functionality**:
  - Verifies the user's credentials against the database.
  - Uses hashed passwords for secure authentication.
  - Stores the user ID in the session upon successful login.
  - Redirects users to the homepage if login is successful, or back to the login page with an error message if unsuccessful.

---

### **6. `logout`**
- **Purpose**: Logs out the currently logged-in user.
- **Functionality**:
  - Removes the user ID from the session.
  - Displays a flash message to indicate the user has been logged out.
  - Redirects the user to the homepage.

---

### **7. `register`**
- **Purpose**: Handles user registration.
- **Functionality**:
  - Collects user information such as username, password, department, and role.
  - Validates the input data.
  - Hashes the user's password for secure storage.
  - Inserts the new user into the `Users` table in the database.
  - Displays a success or error message based on the outcome of the registration process.

---

### **8. `show_user`**
- **Purpose**: Displays information about the currently logged-in user.
- **Functionality**:
  - Fetches user details (ID, username, and role) from the database.
  - Renders the `show_user.html` template to present the user information.
  - Redirects to the login page if no user is logged in.

---

### **9. `app.run(debug=True)`**
- **Purpose**: Starts the Flask application in debug mode for development purposes.
- **Key Points**:
  - Enables debugging features like error stack traces.
  - Automatically reloads the application upon code changes.

---

### **Note**
- **Database Setup**: 
  - The `create_tables` function is called during application startup to ensure the database schema is ready.
  - The `populate_tables` function can be uncommented to populate the database with initial data during the first run.
- **Security**: In production, sensitive information like database credentials and the secret key should be stored in environment variables or configuration files, not hardcoded in the script.

--- 

This structure ensures that the application is modular, scalable, and secure.
