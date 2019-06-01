from flask import Flask, render_template, request, url_for,jsonify
import pymysql.cursors
app = Flask(__name__)


dbconn = pymysql.connect(host='localhost', user='root', password='', db='coffee_shop', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def hello_world():
    with dbconn.cursor() as cursor:
        sql = "SELECT * FROM products ORDER BY sales_number DESC LIMIT 2"
        cursor.execute(sql)
        results_products = cursor.fetchall()

        sql = "SELECT * FROM categories"
        cursor.execute(sql)
        results_categories = cursor.fetchall()

        sql = "SELECT * FROM products"
        cursor.execute(sql)
        results_products_by_category = cursor.fetchall()

        sql = "SELECT * FROM settings"
        cursor.execute(sql)
        results_logo = cursor.fetchone()


    return render_template('index.html',results_categories= results_categories,
                           results_products = results_products,
                           results_products_by_category = results_products_by_category,
                           results_logo = results_logo)


@app.route('/products/<string:id>')
def product_page(id):
    with dbconn.cursor() as cursor:

        sql = "SELECT * FROM products where id = %s"
        cursor.execute(sql,id)
        results_products = cursor.fetchone()

        sql = "SELECT * FROM addons where product_id = %s AND optional LIKE 1"
        cursor.execute(sql,id)
        addons_main = cursor.fetchall()

        sql = "SELECT * FROM addons where product_id = %s AND optional LIKE 2"
        cursor.execute(sql,id)
        addons_optional = cursor.fetchall()

        sql = "SELECT * FROM settings"
        cursor.execute(sql)
        results_logo = cursor.fetchone()

    return render_template("product-page.html", product_name = results_products ,addons_main = addons_main, addons_optional = addons_optional,results_logo = results_logo)


@app.route('/check_order', methods=['GET', 'POST'])
def check_order_session():

        args = request.args

        if "addons_optional" in args:
            addons_optional = args.get("addons_optional")
            print(addons_optional)
        if "addons_main" in args:
            addons_main = args.get("addons_main")
            print(addons_main)

        #        for k, v in args.items():
        #           print(f"{k}: {v}")

        return "Query received: ", 200


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(debug=True)