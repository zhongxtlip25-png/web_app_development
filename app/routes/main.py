from flask import Blueprint, render_template, request
from app.models.recipe import Recipe

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    query = request.args.get('q', '')
    if query:
        # Simple search in title or tags
        recipes = Recipe.query.filter(
            (Recipe.title.contains(query)) | (Recipe.tags.contains(query))
        ).all()
    else:
        recipes = Recipe.get_all()
    return render_template('index.html', recipes=recipes, query=query)
