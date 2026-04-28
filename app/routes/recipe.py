from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.recipe import Recipe, Ingredient, Step
from app import db

bp = Blueprint('recipe', __name__, url_prefix='/recipe')

@bp.route('/<int:id>')
def detail(id):
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash("Recipe not found.", "danger")
        return redirect(url_for('main.index'))
    return render_template('recipe_detail.html', recipe=recipe)

@bp.route('/new', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        if not title:
            flash("Title is required.", "warning")
            return render_template('recipe_form.html', recipe=None)
        
        try:
            data = {
                'title': title,
                'description': request.form.get('description'),
                'portions': request.form.get('portions'),
                'prep_time': request.form.get('prep_time'),
                'cook_time': request.form.get('cook_time'),
                'category': request.form.get('category'),
                'tags': request.form.get('tags'),
                'image_url': request.form.get('image_url')
            }
            recipe = Recipe.create(data)
            
            # Handle ingredients
            ingredient_names = request.form.getlist('ingredient_name[]')
            ingredient_amounts = request.form.getlist('ingredient_amount[]')
            ingredient_units = request.form.getlist('ingredient_unit[]')
            for i in range(len(ingredient_names)):
                if ingredient_names[i]:
                    Ingredient.create({
                        'recipe_id': recipe.id,
                        'name': ingredient_names[i],
                        'amount': ingredient_amounts[i],
                        'unit': ingredient_units[i]
                    })
            
            # Handle steps
            step_descriptions = request.form.getlist('step_description[]')
            for i in range(len(step_descriptions)):
                if step_descriptions[i]:
                    Step.create({
                        'recipe_id': recipe.id,
                        'step_number': i + 1,
                        'description': step_descriptions[i]
                    })
            
            flash("Recipe created successfully!", "success")
            return redirect(url_for('main.index'))
        except Exception as e:
            flash(f"Error creating recipe: {str(e)}", "danger")
            
    return render_template('recipe_form.html', recipe=None)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash("Recipe not found.", "danger")
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        if not title:
            flash("Title is required.", "warning")
            return render_template('recipe_form.html', recipe=recipe)
            
        try:
            data = {
                'title': title,
                'description': request.form.get('description'),
                'portions': request.form.get('portions'),
                'prep_time': request.form.get('prep_time'),
                'cook_time': request.form.get('cook_time'),
                'category': request.form.get('category'),
                'tags': request.form.get('tags'),
                'image_url': request.form.get('image_url')
            }
            Recipe.update(id, data)
            
            # Update ingredients (Simple way: delete and recreate)
            for ing in recipe.ingredients:
                db.session.delete(ing)
            
            ingredient_names = request.form.getlist('ingredient_name[]')
            ingredient_amounts = request.form.getlist('ingredient_amount[]')
            ingredient_units = request.form.getlist('ingredient_unit[]')
            for i in range(len(ingredient_names)):
                if ingredient_names[i]:
                    Ingredient.create({
                        'recipe_id': id,
                        'name': ingredient_names[i],
                        'amount': ingredient_amounts[i],
                        'unit': ingredient_units[i]
                    })
            
            # Update steps (Simple way: delete and recreate)
            for step in recipe.steps:
                db.session.delete(step)
            
            step_descriptions = request.form.getlist('step_description[]')
            for i in range(len(step_descriptions)):
                if step_descriptions[i]:
                    Step.create({
                        'recipe_id': id,
                        'step_number': i + 1,
                        'description': step_descriptions[i]
                    })
            
            db.session.commit()
            flash("Recipe updated successfully!", "success")
            return redirect(url_for('recipe.detail', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating recipe: {str(e)}", "danger")
            
    return render_template('recipe_form.html', recipe=recipe)

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    if Recipe.delete(id):
        flash("Recipe deleted successfully.", "success")
    else:
        flash("Failed to delete recipe.", "danger")
    return redirect(url_for('main.index'))
