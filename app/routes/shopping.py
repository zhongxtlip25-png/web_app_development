from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.shopping import ShoppingItem
from app.models.recipe import Recipe
from app import db

bp = Blueprint('shopping', __name__, url_prefix='/shopping')

@bp.route('/')
def index():
    items = ShoppingItem.get_all()
    return render_template('shopping_list.html', items=items)

@bp.route('/import', methods=['POST'])
def import_from_recipe():
    recipe_id = request.form.get('recipe_id')
    recipe = Recipe.get_by_id(recipe_id)
    if recipe:
        for ing in recipe.ingredients:
            ShoppingItem.create({
                'name': ing.name,
                'amount': ing.amount,
                'unit': ing.unit
            })
        flash(f"Imported ingredients from {recipe.title}", "success")
    else:
        flash("Recipe not found.", "danger")
    return redirect(url_for('shopping.index'))

@bp.route('/<int:id>/toggle', methods=['POST'])
def toggle_status(id):
    item = ShoppingItem.get_by_id(id)
    if item:
        item.is_bought = not item.is_bought
        db.session.commit()
        return {"success": True, "is_bought": item.is_bought}
    return {"success": False}, 404

@bp.route('/clear', methods=['POST'])
def clear_list():
    try:
        ShoppingItem.query.delete()
        db.session.commit()
        flash("Shopping list cleared.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error clearing list: {str(e)}", "danger")
    return redirect(url_for('shopping.index'))
