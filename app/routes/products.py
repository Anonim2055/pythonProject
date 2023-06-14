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


@products.route('/deleteProduct/<_id>', methods=['POST'])
@login_required
def delete_product(_id):
    product_model = Product(db)
    response = product_model.delete_product_by_id(_id)

    if response:
        return redirect(url_for('products.get_my_products'))
    else:
        error = response['error']
        return render_template('myProducts.html', error=error)



@products.route('/myProducts',methods=['GET'])
@login_required
def get_my_products():
    product_model = Product(db)
    response= product_model.get_user_product()
    products = response
    length = len(products)
    return render_template('myProducts.html',products=products,length=length)


@products.route('/updateProduct/<_id>',methods=['GET','POST'])
@login_required
def update_product(_id):
    product_model = Product(db)
    product = product_model.get_product_by_id(_id)
    print(product)
    if request.method == 'GET':
        if 'name' not in product:
            return render_template('not-found.html', error="product not found by id try again or go back...",title="product not found")
        else:
            return render_template('updateProduct.html', product=product)

    if request.method == 'POST':
        body = request.form
        response = product_model.update_by_id(body, _id)
        if response is True:
            return redirect(url_for('products.get_my_products'))
        elif 'error_validate' in response:
            error_validate = response['error_validate']
            print(error_validate)
            return render_template('updateProduct.html', product=product,error=error_validate)
