from . import db

class ShoppingItem(db.Model):
    __tablename__ = 'shopping_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.String(50))
    unit = db.Column(db.String(20))
    is_bought = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'amount': self.amount,
            'unit': self.unit,
            'is_bought': self.is_bought
        }

    @staticmethod
    def create(data):
        try:
            item = ShoppingItem(
                name=data.get('name'),
                amount=data.get('amount'),
                unit=data.get('unit'),
                is_bought=data.get('is_bought', False)
            )
            db.session.add(item)
            db.session.commit()
            return item
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all():
        return ShoppingItem.query.all()

    @staticmethod
    def get_by_id(item_id):
        return ShoppingItem.query.get(item_id)

    @staticmethod
    def update(item_id, data):
        try:
            item = ShoppingItem.query.get(item_id)
            if item:
                item.name = data.get('name', item.name)
                item.amount = data.get('amount', item.amount)
                item.unit = data.get('unit', item.unit)
                item.is_bought = data.get('is_bought', item.is_bought)
                db.session.commit()
            return item
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete(item_id):
        try:
            item = ShoppingItem.query.get(item_id)
            if item:
                db.session.delete(item)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e
