from flask import Blueprint, render_template, request, flash, redirect, url_for,session
from database import db, Payment
from datetime import datetime
from auth import login_required
import pandas as pd
import matplotlib.pyplot as plt

payments_bp = Blueprint('payments', __name__, url_prefix='/payments')


@payments_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register_payment():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        #payment_time = datetime.strptime(request.form['payment_time'], "%Y-%m-%d")
        payment_date = datetime.strptime(request.form['payment_date'], "%Y-%m-%d")


        payee = request.form['payee']
        payment_method = request.form['payment_method']

        if amount < 0 or payment_date > datetime.now():
            flash("Invalid payment information.")
        else:
            payment = Payment(amount=amount, payment_time=payment_date, payee=payee, payment_method=payment_method, user_id=session['user_id'])

            # payment = Payment(amount=amount, payment_time=payment_time, payee=payee, payment_method=payment_method, user_id=session['user_id'])
            db.session.add(payment)
            db.session.commit()
            flash("Payment registered.")
            return redirect(url_for('payments.register_payment'))

    return render_template('register_payment.html')


@payments_bp.route('/query', methods=['GET', 'POST'])
@login_required
def query_payments():
    if request.method == 'POST':
        start_date = datetime.strptime(request.form['start_date'], "%Y-%m-%d")
        end_date = datetime.strptime(request.form['end_date'], "%Y-%m-%d")
        currency = request.form['currency']
        chart_type = request.form['chart_type']  # 获取用户选择的图表类型
        
        queried_payments = Payment.query.filter(Payment.payment_time >= start_date, Payment.payment_time <= end_date)
        
        if currency:
            queried_payments = queried_payments.filter(Payment.currency == currency)
            
        queried_payments = queried_payments.all()

        # 使用pandas创建一个DataFrame来存储查询结果
        df = pd.DataFrame([{
            'payment_date': p.payment_time,
            'amount': p.amount,
            'currency': p.currency,
            'payment_method': p.payment_method
        } for p in queried_payments])

        # 如果用户选择了图表类型并且数据不为空，则生成图表
        if chart_type and not df.empty:
            if chart_type == 'bar':
                # 生成条形图
                df.groupby('payment_date')['amount'].sum().plot(kind='bar')
            elif chart_type == 'pie':
                # 生成饼图
                df.groupby('payment_method')['amount'].sum().plot(kind='pie', autopct='%1.1f%%')
            elif chart_type == 'line':
                # 生成折线图
                df.groupby('payment_date')['amount'].sum().plot(kind='line')

            # 保存生成的图表为PNG文件
            plt.savefig('static/images/payment_chart.png')
            plt.clf()

            # 返回查询结果和图表文件名
            return render_template('query_payments.html', queried_payments=queried_payments, chart_filename='payment_chart.png')
        
    else:
        queried_payments = []
        
    return render_template('query_payments.html', queried_payments=queried_payments)
