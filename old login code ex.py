USERNAME = "karthi"
PASSWORD = "12345678"

# Initialize login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login function
def login(username, password):
    return username == USERNAME and password == PASSWORD

# Show login form if not logged in
if not st.session_state.logged_in:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()

        else:
            st.error("Invalid username or password")
    st.stop()  # Stop the script until login is successful


if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()