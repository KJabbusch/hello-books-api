from app import db

class KpopGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group = db.Column(db.String)
    members = db.Column(db.String)
    label = db.Column(db.String)

    def to_dict(self):
        return {
            'id': self.id,
            'group': self.group,
            'members': self.members,
            'label': self.label
        }