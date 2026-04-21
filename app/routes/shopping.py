from flask import Blueprint, render_template, request, redirect, url_for

shopping_bp = Blueprint('shopping', __name__, url_prefix='/shopping')

@shopping_bp.route('/')
def index():
    """
    顯示購物清單頁面。
    """
    pass

@shopping_bp.route('/import', methods=['POST'])
def import_from_recipe():
    """
    從食譜匯入食材至購物清單。
    Form data: recipe_id
    """
    pass

@shopping_bp.route('/<int:id>/toggle', methods=['POST'])
def toggle_status(id):
    """
    勾選或取消項目的購買狀態。
    """
    pass

@shopping_bp.route('/clear', methods=['POST'])
def clear_list():
    """
    清除所有購物清單項目。
    """
    pass
