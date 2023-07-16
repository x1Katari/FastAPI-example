from tortoise import fields, models

class Cargo(models.Model):
    id = fields.BigIntField(pk=True, index=True)
    cargo_type = fields.CharField(50)
    rate = fields.FloatField()
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField()

    class Meta:
        table = "cargoes"
