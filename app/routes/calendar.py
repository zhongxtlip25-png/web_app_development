from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.calendar import CalendarEvent
from app.models.recipe import Recipe
from app import db
from datetime import datetime

bp = Blueprint('calendar', __name__, url_prefix='/calendar')

@bp.route('/')
def index():
    events = CalendarEvent.get_all()
    recipes = Recipe.get_all()
    return render_template('calendar.html', events=events, recipes=recipes)

@bp.route('/add', methods=['POST'])
def add_event():
    recipe_id = request.form.get('recipe_id')
    event_date_str = request.form.get('event_date')
    meal_type = request.form.get('meal_type')
    
    if not recipe_id or not event_date_str:
        flash("Recipe and Date are required.", "warning")
        return redirect(url_for('calendar.index'))
        
    try:
        event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
        CalendarEvent.create({
            'recipe_id': recipe_id,
            'event_date': event_date,
            'meal_type': meal_type
        })
        flash("Event added to calendar.", "success")
    except Exception as e:
        flash(f"Error adding event: {str(e)}", "danger")
        
    return redirect(url_for('calendar.index'))

@bp.route('/<int:id>/delete', methods=['POST'])
def delete_event(id):
    if CalendarEvent.delete(id):
        flash("Event removed from calendar.", "success")
    else:
        flash("Failed to remove event.", "danger")
    return redirect(url_for('calendar.index'))
