from server import db


class logs(db.Model):
    id = db.column("id",db.Integer,primary_key=True)


