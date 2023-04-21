from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from database import db, CostItem, Payment, CostAllocation
from collections import defaultdict
from datetime import datetime
from auth import login_required
from flask_login import current_user


costs_bp = Blueprint('costs', __name__, url_prefix='/costs')


@costs_bp.route('/summary', methods=['GET', 'POST'])
@login_required
def payment_summary():
    user_id = session['user_id']
    if request.method == 'POST':
        start_date = datetime.strptime(request.form['start_date'], "%Y-%m-%d")
        end_date = datetime.strptime(request.form['end_date'], "%Y-%m-%d")
        summary = defaultdict(float)
        for payment in Payment.query.filter_by(user_id=user_id).all():
            payment_date = payment.payment_time.strftime("%Y-%m-%d")
            if start_date <= datetime.strptime(payment_date, "%Y-%m-%d") <= end_date:
                month = payment.payment_time.strftime("%Y-%m")
                summary[month] += payment.amount
    else:
        summary = defaultdict(float)
        for payment in Payment.query.filter_by(user_id=user_id).all():
            month = payment.payment_time.strftime("%Y-%m")
            summary[month] += payment.amount

    return render_template('payment_summary.html', payment_summary=summary.items())

@costs_bp.route('/allocation', methods=['GET', 'POST'])
@login_required
def cost_allocation():
    if request.method == 'POST':
        cost_item_id = int(request.form['cost_item_id'])
        payment_id = int(request.form['payment_id'])
        amount = float(request.form['amount'])
        allocation_date = datetime.strptime(request.form['allocation_date'], "%Y-%m-%d")

        if amount < 0:
            flash("Invalid cost allocation.")
        else:
            cost_allocation = CostAllocation(cost_item_id=cost_item_id, payment_id=payment_id, amount=amount, allocation_date=allocation_date, user_id=session['user_id'])
            db.session.add(cost_allocation)
            db.session.commit()
            flash("Cost allocation saved.")
            return redirect(url_for('costs.cost_allocation'))

    cost_items = CostItem.query.all()
    payments = Payment.query.all()
    cost_allocations = CostAllocation.query.all()
    return render_template('cost_allocation.html', cost_items=cost_items, payments=payments, cost_allocations=cost_allocations)

@costs_bp.route('/calculation', methods=['GET', 'POST'])
@login_required
def cost_calculation():
    user_id = session['user_id']
    cost_summary = defaultdict(float)

    start_date = None
    end_date = None

    if request.method == 'POST':
        start_date = datetime.strptime(request.form['start_date'], "%Y-%m-%d").date()
        end_date = datetime.strptime(request.form['end_date'], "%Y-%m-%d").date()

    for cost_allocation in CostAllocation.query.filter_by(user_id=user_id).all():
        if request.method == 'POST':
            allocation_date = cost_allocation.allocation_date
            if not (start_date <= allocation_date <= end_date):
                continue

        cost_item_id = cost_allocation.cost_item_id
        cost_summary[cost_item_id] += cost_allocation.amount
        print(f"Adding to cost_summary: {cost_item_id}, Amount: {cost_allocation.amount}")

    for cost_item_id in cost_summary:
        print(f"Cost summary for item {cost_item_id}: {cost_summary[cost_item_id]}")

    cost_items = CostItem.query.filter_by(user_id=user_id).all()
    cost_calculations = [(cost_item.name, cost_summary[cost_item.id]) for cost_item in cost_items]

    return render_template('cost_calculation.html', cost_calculations=cost_calculations)
