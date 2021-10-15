from tortoise import fields, models


class RefreshModel(models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    token = fields.CharField(255)
