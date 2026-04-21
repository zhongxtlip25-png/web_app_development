from . import db
from datetime import date

class CalendarEvent(db.Model):
    __tablename__ = 'calendar_events'
    
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    meal_type = db.Column(db.String(20)) # e.g. breakfast, lunch, dinner

    def to_dict(self):
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'event_date': self.event_date.isoformat(),
            'meal_type': self.meal_type
        }
