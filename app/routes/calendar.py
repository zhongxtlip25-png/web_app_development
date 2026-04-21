from flask import Blueprint, render_template, request, redirect, url_for

calendar_bp = Blueprint('calendar', __name__, url_prefix='/calendar')

@calendar_bp.route('/')
def index():
    """
    顯示烹飪日曆頁面。
    """
    pass

@calendar_bp.route('/add', methods=['POST'])
def add_event():
    """
    將食譜加入日曆排程。
    Form data: recipe_id, event_date, meal_type
    """
    pass

@calendar_bp.route('/<int:id>/delete', methods=['POST'])
def delete_event(id):
    """
    刪除日曆上的特定活動。
    """
    pass
