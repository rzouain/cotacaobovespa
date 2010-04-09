import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from xml.dom import minidom
from httplib2 import Http

class QuoteHandler(webapp.RequestHandler):
  QUOTE_URL = 'http://www.bmfbovespa.com.br/Pregao-Online/ExecutaAcaoAjax.asp?intEstado=1&CodigoPapel=%s'
  http = Http()
  def get(self):
      stock = self.request.get("stock")
      stock = stock.upper()
      (res, content) = self.http.request(self.QUOTE_URL % stock)
      xml = minidom.parseString(content)
      ps = xml.getElementsByTagName('Papel')
      
      preco = None
      erro = None
      if not ps or len(ps) == 0:
        erro = '1'
      else:
        erro = '0'
        papel = ps[0]
        preco = papel.getAttribute('Ultimo')
      
      template_values = {
       'preco': preco,
       'erro': erro,
       'stock': stock,
      }

      path = os.path.join(os.path.dirname(__file__), 'templates/cotacao_bovespa.html')
      self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([('/quote', QuoteHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
