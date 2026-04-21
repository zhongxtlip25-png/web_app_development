from flask import Blueprint, render_template, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁：顯示食譜列表，支援關鍵字搜尋。
    Query args: q (search string)
    """
    pass

@main_bp.route('/recommend')
def recommend():
    """
    食材推薦頁面：根據使用者輸入的食材清單推薦食譜。
    Query args: ingredients (comma separated)
    """
    pass
