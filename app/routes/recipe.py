from flask import Blueprint, render_template, request, redirect, url_for

recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipe')

@recipe_bp.route('/<int:id>')
def detail(id):
    """
    查看食譜詳情頁面。
    """
    pass

@recipe_bp.route('/new', methods=['GET', 'POST'])
def create():
    """
    新增食譜。
    GET: 渲染表單頁。
    POST: 接收資料並存入資料庫。
    """
    pass

@recipe_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    編輯食譜。
    GET: 渲染帶有資料的表單。
    POST: 接收資料並更新。
    """
    pass

@recipe_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除食譜。
    """
    pass
