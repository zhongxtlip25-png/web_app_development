from datetime import datetime
from . import db

class Recipe(db.Model):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    portions = db.Column(db.Integer)
    prep_time = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    image_url = db.Column(db.String(255))
    category = db.Column(db.String(50))
    tags = db.Column(db.String(255)) # Store as comma-separated values
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    ingredients = db.relationship('Ingredient', backref='recipe', cascade='all, delete-orphan', lazy=True)
    steps = db.relationship('Step', backref='recipe', cascade='all, delete-orphan', lazy=True)
    events = db.relationship('CalendarEvent', backref='recipe', cascade='all, delete-orphan', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'portions': self.portions,
            'prep_time': self.prep_time,
            'cook_time': self.cook_time,
            'image_url': self.image_url,
            'category': self.category,
            'tags': self.tags.split(',') if self.tags else [],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @staticmethod
    def create(data):
        """Create a new recipe."""
        try:
            recipe = Recipe(
                title=data.get('title'),
                description=data.get('description'),
                portions=data.get('portions'),
                prep_time=data.get('prep_time'),
                cook_time=data.get('cook_time'),
                image_url=data.get('image_url'),
                category=data.get('category'),
                tags=data.get('tags')
            )
            db.session.add(recipe)
            db.session.commit()
            return recipe
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all():
        """Get all recipes."""
        return Recipe.query.all()

    @staticmethod
    def get_by_id(recipe_id):
        """Get a recipe by ID."""
        return Recipe.query.get(recipe_id)

    @staticmethod
    def update(recipe_id, data):
        """Update a recipe."""
        try:
            recipe = Recipe.query.get(recipe_id)
            if recipe:
                recipe.title = data.get('title', recipe.title)
                recipe.description = data.get('description', recipe.description)
                recipe.portions = data.get('portions', recipe.portions)
                recipe.prep_time = data.get('prep_time', recipe.prep_time)
                recipe.cook_time = data.get('cook_time', recipe.cook_time)
                recipe.image_url = data.get('image_url', recipe.image_url)
                recipe.category = data.get('category', recipe.category)
                recipe.tags = data.get('tags', recipe.tags)
                db.session.commit()
            return recipe
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete(recipe_id):
        """Delete a recipe."""
        try:
            recipe = Recipe.query.get(recipe_id)
            if recipe:
                db.session.delete(recipe)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.String(50))
    unit = db.Column(db.String(20))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'amount': self.amount,
            'unit': self.unit
        }

    @staticmethod
    def create(data):
        try:
            ingredient = Ingredient(
                recipe_id=data.get('recipe_id'),
                name=data.get('name'),
                amount=data.get('amount'),
                unit=data.get('unit')
            )
            db.session.add(ingredient)
            db.session.commit()
            return ingredient
        except Exception as e:
            db.session.rollback()
            raise e

class Step(db.Model):
    __tablename__ = 'steps'
    
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'step_number': self.step_number,
            'description': self.description
        }

    @staticmethod
    def create(data):
        try:
            step = Step(
                recipe_id=data.get('recipe_id'),
                step_number=data.get('step_number'),
                description=data.get('description')
            )
            db.session.add(step)
            db.session.commit()
            return step
        except Exception as e:
            db.session.rollback()
            raise e
