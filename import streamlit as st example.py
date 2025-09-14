import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd

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


# Sample in-memory "database"
if 'products' not in st.session_state:
    st.session_state.products = []

# Helper function find product by ID
def get_product_by_id(product_id):
    for product in st.session_state.products:
        if product['id'] == product_id:
            return product
    return None

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="PRODUCT MANAGEMENT",
        options=["Create", "Read", "Update", "Delete"],
        icons=["house", "eye", "pencil", "trash"]
    )

st.title("Product Management")

# ------------------------ CREATE ------------------------
if selected == "Create":
    st.subheader("Add New Product")

    product_id = st.text_input("Product ID")
    name = st.text_input("Product Name")
    price = st.number_input("Price", min_value=0.0, format="%.2f")
    stock = st.number_input("Stock", step=1)
    warranty_month = st.number_input("Warranty (in months)", step=1)
    rating = st.slider("Rating", min_value=0.0, max_value=9.0, step=0.1)

    if st.button("Add Product"):
        if get_product_by_id(product_id):
            st.warning("Product ID already exists!")
        else:
            st.session_state.products.append({
                'id': product_id,
                'name': name,
                'price': price,
                'stock': stock,
                'warranty_month': warranty_month,
                'rating': rating
            })
            st.success(" Product added successfully!")

# ------------------------ READ ------------------------
elif selected == "Read":
    st.subheader("Product List")

    if not st.session_state.products:
        st.info("No products available.")
    else:
        df = pd.DataFrame(st.session_state.products)
        st.dataframe(df)

        #save csv file
        file_path = "products.csv"
        df.to_csv(file_path,index=False)

        #download button
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
    label="Download Products",
    data=csv,
    file_name="products.csv",
    mime="text/csv"
)
        
        

# ------------------------ UPDATE ------------------------
elif selected == "Update":
    st.subheader("Update Product")

    ids = [p['id'] for p in st.session_state.products]
    if not ids:
        st.info("No products to update.")
    else:
        selected_id = st.selectbox("Select Product ID", ids)
        product = get_product_by_id(selected_id)

        if product:
            new_name = st.text_input("Product Name", value=product['name'])
            new_price = st.number_input("Price", value=product['price'], format="%.2f")
            new_stock = st.number_input("Stock", value=product['stock'], step=1)
            new_warranty_month = st.number_input("Warranty (in months)", value=product['warranty_month'], step=1)
            new_rating = st.slider("Rating", min_value=0.0, max_value=9.0, step=0.1, value=product['rating'])

            if st.button("Update Product"):
                product['name'] = new_name
                product['price'] = new_price
                product['stock'] = new_stock
                product['warranty_month'] = new_warranty_month
                product['rating'] = new_rating
                st.success("Product updated successfully!")

# ------------------------ DELETE ------------------------
elif selected == "Delete":
    st.subheader("Delete Product")

    ids = [p['id'] for p in st.session_state.products]
    if not ids:
        st.info("No products to delete.")
    else:
        selected_id = st.selectbox("Select Product ID to Delete", ids)

        if st.button("Delete Product"):
            st.session_state.products = [p for p in st.session_state.products if p['id'] != selected_id]
            st.success(f" Product '{selected_id}' deleted.")