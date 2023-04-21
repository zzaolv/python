from flask import Blueprint, render_template
from flask import request, redirect, url_for, flash, session
from database import db, User
from datetime import datetime
from auth import login_required
from flask import Blueprint, render_template, session
from .weather import get_ip_info, get_weather
#from database import User
#from .weather import  get_ip, get_city_by_ip,get_weather
bp = Blueprint('main_window', __name__, url_prefix='/main')

@bp.route('/')
@login_required  # 添加这个装饰器
def main():
    user_id = session['user_id']
    user = User.query.get(session['user_id'])
    #user = User.query.get(user_id)
    #user = User.query.filter_by(id=session['user_id']).first()
    api_key = 'b5c8bde6f6899b30c8e83d7193653367'  # Replace with your OpenWeatherMap API key
    ip_info = get_ip_info()
    if ip_info:
        city = ip_info['city']
    else:
        city = 'your_default_city_here'  # Replace with your default city name

    weather = get_weather(city, api_key)
    #is_admin = user.is_admin  # Add this line
    #return render_template('main_window.html', weather=weather)
    return render_template('main_window.html', datetime=datetime, user=user, weather=weather,session=session)
@bp.route('/')
@login_required
def main_view():
    user = User.query.get(session['user_id'])
    return render_template('main_window.html', datetime=datetime)
