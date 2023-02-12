from tortoise import fields, models

__all__ = ("Guild",)


class Guild(models.Model):
    class Meta:
        table = "guilds"

    guild_id = fields.BigIntField(pk=True, index=True, generated=False)

    prefix = fields.CharField(default="q", max_length=5)
    embed_color = fields.IntField(default=65459, null=True)
    embed_footer = fields.TextField(default="Quotient • quotientbot.xyz")

    is_premium = fields.BooleanField(default=False)
    made_premium_by = fields.BigIntField(null=True)
    premium_end_time = fields.DatetimeField(null=True)

    public_profile = fields.BooleanField(default=True)  # whether to list the server on global leaderboards
