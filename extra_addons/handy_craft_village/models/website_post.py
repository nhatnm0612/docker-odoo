import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.http_routing.models.ir_http import slug


class WebsitePost(models.Model):
    _name = 'website.post'
    _inherit = ['website.published.mixin']

    name = fields.Char(
        string='Title',
        translate=True,
        required=True,
    )
    image = fields.Image(
        string='Post Image'
    )
    content = fields.Html(
        string='Content',
        translate=True
    )
    short_content = fields.Char(
        string='Short Content',
        compute='_compute_short_content',
        size=205
    )
    is_quiz = fields.Boolean(
        string='Quiz?'
    )
    allow_using_image_for_carousel = fields.Boolean()
    answer_ids = fields.One2many(
        comodel_name='website.post.answer',
        inverse_name='post_id',
        string='Answers'
    )

    @api.depends_context('lang')
    @api.depends('content')
    def _compute_short_content(self):
        lang = self._context.get('lang')
        for r in self:
            short_content = ''
            if r.content and r.content.__str__():
                content_short = re.sub(r'<.*?>', '', r.with_context(lang=lang).content[:200])
                short_content = content_short + '...'
            r.short_content = short_content

    @api.constrains('answer_ids', 'is_quiz', 'answer_ids.correct')
    def _check_answers(self):
        for r in self:
            if not r.is_quiz:
                continue
            if not r.answer_ids:
                raise ValidationError(_('Quiz needs answers!'))
            if len(r.answer_ids.filtered(lambda wpa: wpa.correct)) != 1:
                raise ValidationError(_('Quiz required 1 correct answer!'))
            if all(r.answer_ids.mapped('correct')):
                raise ValidationError(_('Quiz needs wrong answer!'))

    @api.constrains('allow_using_image_for_carousel', 'image')
    def _check_allow_using_image_for_carousel(self):
        for r in self:
            if r.allow_using_image_for_carousel and not r.image:
                raise ValidationError(_('Need image for carousel!'))

    def _compute_website_url(self):
        super()._compute_website_url()
        for r in self:
            website_url = False
            if r.id and r.name:
                website_url = '/posts/%s' % slug(r)
            r.website_url = website_url

    def _get_correct_answer(self):
        self.ensure_one()
        if not self.is_quiz:
            return
        return self.answer_ids.filtered(lambda wpa: wpa.correct).id
