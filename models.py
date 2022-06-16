from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class APIKeys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), unique=True, nullable=False)
    value = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f"<APIKeys {self.name}>"

    @property
    def serialize(self):
        return ( self.key, self.value )

    @property
    def serialize_many2many(self):
        return [ item.serialize for item in self.many2many]

class PublicItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    color = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f"<PublicItem {self.name}>"

    @property
    def serialize(self):
        return {
            'id':    self.id,
            'name':  self.name,
            'color': self.color
        }

