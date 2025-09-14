def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",           # Your MySQL username
        password="karthi@007", # Your MySQL password
        database="products"    # Make sure this database exists
    )

# Create users table if not exists
def create_users_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE,
            password VARCHAR(255)
        )
    """)
    conn.commit()
    conn.close()

create_users_table()

# ------------------- USER FUNCTIONS -------------------
def signup_user(username, password):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        conn.close()
        return True
    except mysql.connector.IntegrityError:
        return False

def login_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# ------------------- SESSION STATE -------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ------------------- AUTHENTICATION -------------------
if not st.session_state.logged_in:
    st.title("🔐 User Authentication")

    menu = st.radio("Select Action", ["Login", "Sign Up"], horizontal=True)

    if menu == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"✅ Welcome, {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

    elif menu == "Sign Up":
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Sign Up"):
            if new_password != confirm_password:
                st.warning("⚠️ Passwords do not match!")
            elif signup_user(new_username, new_password):
                st.success("🎉 Sign Up successful! Please log in now.")
            else:
                st.error("⚠️ Username already exists!")

    st.stop()  # Stop script until login is successful

# ------------------- LOGOUT -------------------
st.sidebar.write(f"👋 Hello, {st.session_state.username}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()