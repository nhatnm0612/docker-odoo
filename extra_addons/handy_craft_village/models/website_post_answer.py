from odoo import _, api, fields, models


class WebsitePostAnswer(models.Model):
    _name = 'website.post.answer'
    _order = 'post_id, name'

    post_id = fields.Many2one(
        comodel_name='website.post',
        string='Quiz Post',
        required=True,
        readonly=True,
        ondelete='cascade'
    )
    name = fields.Char(
        string='Answer',
        translate=True,
        required=True
    )
    correct = fields.Boolean(
        string='Correct?'
    )

    _sql_constraints = [
        (
            'post_id_name_uniq',
            'UNIQUE(post_id, name)',
            'Answer should be unique per quiz!'
        )
    ]
