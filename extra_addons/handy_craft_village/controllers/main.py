from odoo import http, fields
from odoo.http import request

from odoo.addons.website.controllers.main import Website


class HandyCraftVillageWebsite(Website):

    @http.route('/quiz', type='http', auth='public', website=True)
    def quiz_route(self, **kw):
        Post = request.env['website.post'].with_context(lang=request._context.get('lang', 'vi_VN'))
        last_10_quizes = Post.search(
            [('is_quiz', '=', True)],
            limit=10,
            order='id desc'
        )
        if not last_10_quizes:
            raise request.not_found()
        return request.render('handy_craft_village.quiz', {'quizes': last_10_quizes})

    @http.route('/quiz/answer', type='http', auth='public', website=True)
    def quiz_aswer_route(self, **kw):
        quiz_ids = list(map(int, kw.keys()))
        quizes = request.env['website.post'].browse(quiz_ids)
        corrects_count = 0
        for quiz in quizes:
            correct_answer_id = quiz._get_correct_answer()
            if kw.get(str(quiz.id)) == str(correct_answer_id):
                corrects_count += 1
        return request.render('handy_craft_village.quiz_answer',
            {'corrects_count': corrects_count, 'quizes_count': len(quizes)}
        )

    @http.route('/posts/<model("website.post"):post>', type='http', auth='public', website=True)
    def post_route(self, post, **kw):
        if not post or post.is_quiz:
            raise request.not_found()
        return request.render('handy_craft_village.post', {'post': post})

    @http.route('/')
    def index(self, **kw):
        super().index(**kw)
        Post = request.env['website.post'].with_context(lang=request._context.get('lang', 'vi_VN'))
        last_10_posts = Post.search(
            [('is_quiz', '=', False)],
            limit=10,
            order='id desc'
        )
        last_3_carousel_images = Post.search(
            [('allow_using_image_for_carousel', '=', True)],
            limit=3,
            order='id desc'
        )
        return request.render('handy_craft_village.homepage', {
            'post': last_10_posts,
            'carousel': last_3_carousel_images
        })
