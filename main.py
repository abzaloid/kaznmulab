# coding=utf-8

import webapp2
import jinja2
import os

from google.appengine.api import mail

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template))

class MainHandler(Handler):
    def get(self):
    	self.render("index.html")

    def post(self):
        message = mail.EmailMessage()
        message.sender = self.request.get('name') + ' <abzal.serekov@gmail.com>'
        message.to = "abzal.serekov@gmail.com"
        message.subject = "kaznmulab"
        message.body = self.request.get('message') + "\n" + "from : " + self.request.get('e-mail')
        message.send()


        message = mail.EmailMessage()
        message.sender = self.request.get('name') + ' <abzal.serekov@gmail.com>'
        message.to = "aserekov@gmail.com"
        message.subject = "kaznmulab"
        message.body = self.request.get('message') + "\n" + "from : " + self.request.get('e-mail')
        message.send()

        self.redirect('/')


def handle_404(request, response, exception):
	response.write('Ошибка 404: Не найдена страница<br/><a href="/">Перейти на главную страницу</a>')
	response.set_status(404)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

app.error_handlers[404] = handle_404