from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png'])

@app.route('/')
def home():
    return render_template("add.html")

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    if request.method == "POST":
        name = request.form['name']
        price = float(request.form['price'])
        stock = int([request.form['stock']])
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(filename))
        imagename = filename
        with sqlite3.connect('database.db') as conn:
            try:
                cur = conn.cursor
                cur.execute('''INSERT INTO products (name, price, image, stock) VALUES (?, ?, ?, ?, ?, ?)''', (name, price, imagename, stock))
                conn.commit()
                msg="added successfully"
            except:
                msg="error occured"
                conn.rollback()
        conn.close()
        print(msg)

@app.route("/productDescription")
def productDescription():
    productId = request.args.get('productId')
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, image, stock FROM products WHERE productId = ?', (productId))
        productData = cur.fetchone()
    conn.close()
    return render_template("products.html", data=productData)

def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans
        

if __name__ == '__main__':
    app.run(debug=True)