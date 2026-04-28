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

    @staticmethod
    def create(data):
        try:
            event = CalendarEvent(
                recipe_id=data.get('recipe_id'),
                event_date=data.get('event_date'),
                meal_type=data.get('meal_type')
            )
            db.session.add(event)
            db.session.commit()
            return event
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all():
        return CalendarEvent.query.all()

    @staticmethod
    def get_by_id(event_id):
        return CalendarEvent.query.get(event_id)

    @staticmethod
    def update(event_id, data):
        try:
            event = CalendarEvent.query.get(event_id)
            if event:
                event.recipe_id = data.get('recipe_id', event.recipe_id)
                event.event_date = data.get('event_date', event.event_date)
                event.meal_type = data.get('meal_type', event.meal_type)
                db.session.commit()
            return event
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete(event_id):
        try:
            event = CalendarEvent.query.get(event_id)
            if event:
                db.session.delete(event)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e
