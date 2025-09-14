import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
from mysql.connector import Error


# ------------------ DB CONNECTION ------------------
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Yogaraj@11",  # Your MySQL password
            database="products"
        )
        return conn
    except Error as e:
        st.error(f"Database connection failed: {e}")
        return None

# ------------------ CREATE USERS TABLE ------------------
def create_users_table():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()

# ------------------ ADD USER (SIGNUP) ------------------
def add_user(username, password):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Error as e:
            st.error(f"Error: {e}")
            return False

# ------------------ LOGIN USER ------------------
def login_user(username, password):
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    return None

# ------------------ CREATE PRODUCTS TABLE ------------------
def create_products_table():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_list (
                id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100),
                price FLOAT,
                stock INT,
                warranty_month INT,
                rating FLOAT
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()

# ------------------ ADD PRODUCT ------------------
def add_product(product_id, name, price, stock, warranty_month, rating):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO product_list (id, name, price, stock, warranty_month, rating)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (product_id, name, price, stock, warranty_month, rating))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Error as e:
            st.error(f"Error: {e}")
            return False

# ------------------ GET ALL PRODUCTS ------------------
def get_all_products():
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM product_list")
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return products
    return []

# ------------------ DELETE PRODUCT ------------------
def delete_product(product_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM product_list WHERE id=%s", (product_id,))
        conn.commit()
        cursor.close()
        conn.close()

# ------------------ UPDATE PRODUCT ------------------
def update_product(product_id, name, price, stock, warranty_month, rating):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE product_list 
            SET name=%s, price=%s, stock=%s, warranty_month=%s, rating=%s
            WHERE id=%s
        """, (name, price, stock, warranty_month, rating, product_id))
        conn.commit()
        cursor.close()
        conn.close()

# ------------------ INITIALIZE ------------------
create_users_table()
create_products_table()

# ------------------ SESSION STATES ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "login"

# ------------------ LOGIN PAGE ------------------
if not st.session_state.logged_in and st.session_state.page == "login":
    st.title(" Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = user["username"]
            st.success(f"Welcome {user['username']} ")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password!")

    if st.button("Signup"):
        st.session_state.page = "signup"
        st.experimental_rerun()

    st.stop()

# ------------------ SIGNUP PAGE ------------------
elif not st.session_state.logged_in and st.session_state.page == "signup":
    st.title(" Signup Page")

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")

    if st.button("Create Account"):
        if add_user(new_username, new_password):
            st.success("Account created successfully! Please login.")
            st.session_state.page = "login"
            st.experimental_rerun()
        else:
            st.error("Username already exists!")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.experimental_rerun()

    st.stop()

# ------------------ PRODUCT MANAGEMENT ------------------
with st.sidebar:
    selected = option_menu(
        menu_title="PRODUCT MANAGEMENT",
        options=["Create", "Read", "Update", "Delete"],
        icons=["plus-circle", "eye", "pencil", "trash"]
    )

st.title("Product Management")

# CREATE PRODUCT
if selected == "Create":
    st.subheader("Add New Product")
    product_id = st.text_input("Product ID")
    name = st.text_input("Product Name")
    price = st.number_input("Price", min_value=0.0, format="%.2f")
    stock = st.number_input("Stock", step=1)
    warranty_month = st.number_input("Warranty (Months)", step=1)
    rating = st.slider("Rating", 0.0, 9.0, step=0.1)

    if st.button("Add Product"):
        if add_product(product_id, name, price, stock, warranty_month, rating):
            st.success("Product added successfully!")
        else:
            st.error("Product ID already exists!")

# READ PRODUCTS
elif selected == "Read":
    st.subheader("Product List")
    products = get_all_products()
    if products:
        df = pd.DataFrame(products)
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Products",
            data=csv,
            file_name="products.csv",
            mime="text/csv"
        )
    else:
        st.info("No products available.")

# UPDATE PRODUCT
elif selected == "Update":
    st.subheader("Update Product")
    products = get_all_products()
    ids = [p['id'] for p in products]

    if ids:
        selected_id = st.selectbox("Select Product ID", ids)
        product = next((p for p in products if p['id'] == selected_id), None)

        if product:
            new_name = st.text_input("Product Name", value=product['name'])
            new_price = st.number_input("Price", value=product['price'], format="%.2f")
            new_stock = st.number_input("Stock", value=product['stock'], step=1)
            new_warranty = st.number_input("Warranty (Months)", value=product['warranty_month'], step=1)
            new_rating = st.slider("Rating", 0.0, 9.0, value=product['rating'], step=0.1)

            if st.button("Update Product"):
                update_product(selected_id, new_name, new_price, new_stock, new_warranty, new_rating)
                st.success("Product updated successfully!")
    else:
        st.info("No products available to update.")

# DELETE PRODUCT
elif selected == "Delete":
    st.subheader("Delete Product")
    products = get_all_products()
    ids = [p['id'] for p in products]

    if ids:
        selected_id = st.selectbox("Select Product ID to Delete", ids)
        if st.button("Delete Product"):
            delete_product(selected_id)
            st.success(f"Product '{selected_id}' deleted successfully!")
    else:
        st.info("No products available to delete.")

# LOGOUT
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.page = "login"
    st.experimental_rerun()




# # Connect to MySQL
# conn = mysql.connector.connect(
#     host="localhost",      # Or your MySQL server
#     user="root",           # Your MySQL username
#     password="Yogaraj@11",  # Your MySQL password
#     database="products"    # Your database name
    
# )
# cursor = conn.cursor()

# # Create table (if not exists)
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS products (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100),
#     price FLOAT,
#     stock INT,
#     Warranty_month INT,
#     rating Float           
# )
# """)
# conn.commit()

# # CREATE
# name = st.text_input("enter product name")
# stock = st.number_input("enter stock",min_value=0,max_value=1000,step=1)
# price = st.number_input("enter price",min_value=0.0,step=0.01) 
# Warranty_month = st.number_input("enter Warranty(in months)",min_value=0,step=1)
# rating = st.number_input("enter rating",min_value=0.0,max_value=5.0,step=0.1)

# if st.button("Add product"):
#      if name:
#       cursor.execute("INSERT INTO products (name, stock, price, warranty_month, rating ) VALUES (%s, %s, %s, %s, %s)", (name, stock, price, Warranty_month, rating))
#       conn.commit()
#       st.success("product added success.")
#      else:
#       st.warning("please enter product name")


# # view
# st.subheader("view all products")
# if st.button("show all products"):
#      cursor.execute("select * from products")
#      rows = cursor.fetchall()
#      for row in rows:
#         st.write(f"id:{row[0]} | name:{row[1]} | stock:{row[2]} | price:{row[3]} | Warranty:{row[4]}months | rating{row[5]}")
        

# # UPDATE
#      st.subheader("update products")
#      update_id = st.number_input("enter product id ",min_value=1, step=1)
#      new_stock = st.number_input("new stock", min_value=0,key="update_stock")
#      new_price = st.number_input("new price",min_value=0.0, step=0.01,key="update_price")
#      new_warranty = st.number_input("new Warranty (month)",min_value=0, step=1, key="update_warranty")
#      new_rating = st.number_input("new rating", value=0.0 , min_value=0.0, max_value=5.0,step=0.1,key="update_rating")

# if st.button("update products"):
#      cursor.execute(""" UPDATE products
#         SET stock = %s, price = %s, Warranty_month = %s, rating = %s
#         WHERE id = %s """, (new_stock, new_price, new_warranty, new_rating, update_id))
#      conn.commit()
#      st.success("product update successfully ")



# # DELETE
# st.subheader("delete product")
# delete_id = st.number_input("enter product id to delete ", min_value=1, step=1, key="delete_id")
# if st.button("delete"):
#      cursor.execute("delete from products where id= %s",(delete_id,))
#      conn.commit()
#      st.success("product delete") 