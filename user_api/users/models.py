from tortoise import fields, models


class UserModel(models.Model):
    """A user to connect to the service"""

    id = fields.IntField(pk=True)
    email = fields.CharField(255)
    password = fields.CharField(255)
    birth_date = fields.DateField()
    first_name = fields.CharField(100)
    last_name = fields.CharField(100)
