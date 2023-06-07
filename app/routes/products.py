from ..main import db
from flask import Blueprint,jsonify,request,render_template,redirect,url_for,session
products = Blueprint('products',__name__,url_prefix='/products')
from ..models.productModel import Product
from ..middleware.authorization import login_required
@products.route('', methods=['GET'])
def get_all_products():
    return jsonify({"msg":"Products is working"})


@products.route('/addProduct',methods=['GET','POST'])
@login_required
def add_product():
    if request.method == 'POST':
        body = request.form
        product_model = Product(db)
        response = product_model.create(body)
        if response:
             return redirect(url_for('products.get_my_products'))
        else:
            error =response
            return render_template('addProduct.html',error = error)

    if request.method == "GET":
        return render_template('addProduct.html',error=None)


@products.route('/myProducts',methods=['GET'])
def get_my_products():
    product_model = Product(db)
    response= product_model.get_user_product()
    products = response
    return render_template('myProducts.html',products=products)