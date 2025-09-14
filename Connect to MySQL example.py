# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",      # Or your MySQL server
    user="root",           # Your MySQL username
    password="karthi@007",  # Your MySQL password
    database="products"    # Your database name
    
)
cursor = conn.cursor()

# Create table (if not exists)
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    price FLOAT,
    stock INT,
    Warranty_month INT,
    rating Float           
)
               
               
""")
conn.commit()

# CREATE
name = st.text_input("enter product name")
stock = st.number_input("enter stock",min_value=0,max_value=1000,step=1)
price = st.number_input("enter price",min_value=0.0,step=0.01) 
Warranty_month = st.number_input("enter Warranty(in months)",min_value=0,step=1)
rating = st.number_input("enter rating",min_value=0.0,max_value=5.0,step=0.1)

if st.button("Add product"):
    if name:
     cursor.execute("INSERT INTO products (name, stock, price, warranty_month, rating ) VALUES (%s, %s, %s, %s, %s)", (name, stock, price, Warranty_month, rating))
    conn.commit()
    st.success("product added success.")
else:  
     st.warning("please enter product name")

# view
st.subheader("view all products")
if st.button("show all products"):
    cursor.execute("select * from products")
    rows = cursor.fetchall()
    for row in rows:
        st.write(f"id:{row[0]} | name:{row[1]} | stock:{row[2]} | price:{row[3]} | Warranty:{row[4]}months | rating{row[5]}")
        

# UPDATE

st.subheader("update products")
update_id = st.number_input("enter product id ",min_value=1, step=1)
new_stock = st.number_input("new stock", min_value=0,key="update_stock")
new_price = st.number_input("new price",min_value=0.0, step=0.01,key="update_price")
new_warranty = st.number_input("new Warranty (month)",min_value=0, step=1, key="update_warranty")
new_rating = st.number_input("new rating", value=0.0 , min_value=0.0, max_value=5.0,step=0.1,key="update_rating"

if st.button("update products"):
    cursor.execute(""" UPDATE products
        SET stock = %s, price = %s, Warranty_month = %s, rating = %s
        WHERE id = %s """, (new_stock, new_price, new_warranty, new_rating, update_id))
    conn.commit()
    st.success("product update successfully ")



# DELETE
st.subheader("delete product")
delete_id = st.number_input("enter product id to delete ", min_value=1, step=1, key="delete_id")
if st.button("delete"):
    cursor.execute("delete from products where id= %s",(delete_id,))
    conn.commit()
    st.success("product delete")
