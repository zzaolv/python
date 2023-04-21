from flask import Blueprint, render_template
from auth import login_required
bp = Blueprint('expense_management', __name__, url_prefix='/expense_management')

@bp.route('/')
@login_required  # 添加这个装饰器
def index():
    return render_template('expense_management.html')
