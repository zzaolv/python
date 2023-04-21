from flask import Blueprint, render_template, request, flash, redirect, session, url_for,send_file
from database import db, PaymentContract, NonPaymentContract, CostItem,User
from datetime import datetime
import os
import pandas as pd
from werkzeug.utils import secure_filename
from flask_login import current_user,login_required
from auth import login_required


contracts_bp = Blueprint('contracts', __name__, url_prefix='/contracts')
ALLOWED_EXTENSIONS = {'xlsx'}


@contracts_bp.route('/payment', methods=['GET', 'POST'])
@login_required
def payment_contract():

    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        payment_time = datetime.strptime(request.form['payment_time'], "%Y-%m-%d")
        payment_method = request.form['payment_method']
        
        if amount < 0 or payment_time > datetime.now():
            flash("Invalid contract information.")
        else:
            payment_contract = PaymentContract(name=name, amount=amount, payment_time=payment_time, payment_method=payment_method, user_id=session['user_id'])
            db.session.add(payment_contract)
            db.session.commit()
            flash("Payment contract registered.")
            return redirect(url_for('contracts.payment_contract'))

    return render_template('payment_contract.html')


@contracts_bp.route('/non_payment', methods=['GET', 'POST'])
@login_required
def non_payment_contract():
    current_username = session['username']
    user = User.query.filter_by(username=current_username).first()

    if request.method == 'POST':
        name = request.form['contract_name']
        cost_item_id = int(request.form['cost_item_id'])
        amount = float(request.form['amount'])

        if amount < 0:
            flash("Invalid contract information.")
        else:
            non_payment_contract = NonPaymentContract(name=name, cost_item_id=cost_item_id, amount=amount, user_id=session['user_id'])
            db.session.add(non_payment_contract)
            db.session.commit()
            flash("Non-payment contract registered.")
            return redirect(url_for('contracts.non_payment_contract'))

    cost_items = CostItem.query.all()
    return render_template('non_payment_contract.html',  cost_items=cost_items)



@contracts_bp.route('/cost_items', methods=['GET', 'POST'])
@login_required
def cost_items():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        description = request.form['description']

        cost_item = CostItem(name=name, code=code, description=description, user_id=session['user_id'])
        db.session.add(cost_item)
        db.session.commit()
        flash("Cost item added.")
        return redirect(url_for('contracts.cost_items'))

    cost_items = CostItem.query.all()
    return render_template('cost_items.html', cost_items=cost_items)

@contracts_bp.route('/export_payment_contracts', methods=['GET'])
@login_required
def export_payment_contracts():
    payment_contracts = PaymentContract.query.all()
    data = {
        "Contract Name": [contract.name for contract in payment_contracts],
        "Contract Amount": [contract.amount for contract in payment_contracts],
        "Payment Time": [contract.payment_time for contract in payment_contracts],
        "Payment Method": [contract.payment_method for contract in payment_contracts]
    }
    df = pd.DataFrame(data)
    file_path = 'payment_contracts_export.xlsx'
    df.to_excel(file_path, index=False)

    return send_file(file_path, as_attachment=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@contracts_bp.route('/import_payment_contracts', methods=['GET', 'POST'])
@login_required
def import_payment_contracts():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file_path = os.path.join('uploads', secure_filename(file.filename))
            file.save(file_path)

            df = pd.read_excel(file_path)
            for _, row in df.iterrows():
                name = row['Contract Name']
                amount = row['Contract Amount']
                payment_time = row['Payment Time']
                payment_method = row['Payment Method']

                payment_contract = PaymentContract(name=name, amount=amount, payment_time=payment_time, payment_method=payment_method, user_id=session['user_id'])
                db.session.add(payment_contract)

            db.session.commit()
            flash("Payment contracts imported.")
            return redirect(url_for('contracts.payment_contract'))

    return render_template('import_payment_contracts.html')
