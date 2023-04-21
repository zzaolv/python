from flask import Blueprint, render_template
from auth import login_required
bp = Blueprint('payment_management', __name__, url_prefix='/payment_management')

@bp.route('/')
@login_required  # 添加这个装饰器
def index():
    return render_template('payment_management.html')
