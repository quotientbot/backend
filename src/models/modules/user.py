from tortoise import fields, models

__all__ = ("User", "Vote")


class User(models.Model):
    class Meta:
        table = "users"

    user_id = fields.BigIntField(pk=True, index=True, generated=False)

    is_premium = fields.BooleanField(default=False, index=True)
    premium_expire_time = fields.DatetimeField(null=True)

    public_profile = fields.BooleanField(default=True)
    quocoins = fields.IntField(default=0)

    vote_reminder = fields.BooleanField(default=False)
    votes: fields.ManyToManyRelation["Vote"] = fields.ManyToManyField("models.Vote")


class Vote(models.Model):
    class Meta:
        table = "votes"

    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now=True)
    expires_at = fields.DatetimeField()
