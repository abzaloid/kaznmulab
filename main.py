# coding=utf-8

import webapp2
import jinja2
import os
import json
import caching
import models
from google.appengine.ext import db
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
        self.write(self.render_str(template, **kw))

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

class DatabaseHandler(Handler):
    def get(self):
        names = ['bi', 'oik', 'bik', 'isg', 'diz']
        russian = [u'БАКТЕРИОЛОГИЧЕСКИЕ ИССЛЕДОВАНИЯ',
        u'ОБЩЕКЛИНИЧЕСКИЕ ИССЛЕДОВАНИЯ КРОВИ',
        u'БИОХИМИЧЕСКИЕ ИССЛЕДОВАНИЯ КРОВИ',
        u'ИССЛЕДОВАНИЕ СОДЕРЖАНИЯ ГОРМОНОВ',
        u'ДИАГНОСТИКА ИНФЕКЦИОННЫХ ЗАБОЛЕВАНИЙ']
        for i in range(5):
            f = open("parse/"+names[i]+".json", "r")
            items = json.loads(''.join(line for line in f))
            f.close()
            for item in items:
                if i == 0:
                    t = models.BI(name = item['name'], category=item['category'], price=item['price'], parentt=item['parent'])
                if i == 1:
                    t = models.OIK(name = item['name'], category=item['category'], price=item['price'], parentt=item['parent'])
                if i == 2:
                    t = models.BIK(name = item['name'], category=item['category'], price=item['price'], parentt=item['parent'])
                if i == 3:
                    t = models.ISG(name = item['name'], category=item['category'], price=item['price'], parentt=item['parent'])
                if i == 4:
                    t = models.DIZ(name = item['name'], category=item['category'], price=item['price'], parentt=item['parent'])
                t.put()
        self.write('done!')

class PriceListHandler(Handler):
    def get(self):
        self.render('price_list.html', category="oik", data=caching.get_oik())
    def post(self):
        pass

class BIHandler(Handler):
    def get(self):
        self.render('price_list.html', category="bi", data=caching.get_bi())

class BIKHandler(Handler):
    def get(self):
        self.render('price_list.html', category="bik", data=caching.get_bik())

class OIKHandler(Handler):
    def get(self):
        self.render('price_list.html', category="oik", data=caching.get_oik())

class DIZHandler(Handler):
    def get(self):
        self.render('price_list.html', category="diz", data=caching.get_diz())

class ISGHandler(Handler):
    def get(self):
        self.render('price_list.html', category="isg", data=caching.get_isg())

class AboutHandler(Handler):
    def get(self):
        self.render('about.html')

def handle_404(request, response, exception):
	response.write('Ошибка 404: Не найдена страница<br/><a href="/">Перейти на главную страницу</a>')
	response.set_status(404)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/price_list', PriceListHandler),
    ('/database_update', DatabaseHandler),
    ('/bi', BIHandler),
    ('/bik', BIKHandler),
    ('/oik', OIKHandler),
    ('/isg', ISGHandler),
    ('/diz', DIZHandler),
    ('/about', AboutHandler),
], debug=True)

app.error_handlers[404] = handle_404