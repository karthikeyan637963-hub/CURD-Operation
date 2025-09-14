# Example login & signup functions (replace with your MySQL logic)
def login_user(username, password):
    return username == "admin" and password == "1234"

def signup_user(username, password):
    # Example: insert into DB if not exists
    return True

# Initialize session state
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

st.title("LOGIN ")

# ------------------ LOGIN FORM ------------------ #
if not st.session_state.show_signup:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(" LOGIN successfully")
            st.rerun()
        else:
            st.error(" Invalid username or password")

    # Button to switch to Sign Up form
    if st.button("Sign Up"):
        st.session_state.show_signup = True
        st.rerun()

# ------------------ SIGN UP FORM ------------------ #
else:
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Back to Login"):
        st.session_state.show_signup = False
        st.rerun()


# ------------------- LOGOUT -------------------
st.sidebar.write(f"Hello, {st.session_state.username}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()