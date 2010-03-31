import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
import yql

class QuoteHandler(webapp.RequestHandler):
  
  def get(self):
      stock = self.request.get("stock")
      stock = stock.upper()
      y = yql.Public()
      q = "select * from html where xpath='//td[@class=\"tdValor\"]/p' and url='http://www.bmfbovespa.com.br/Cotacao-Rapida/ExecutaAcaoCotRapXSL.asp?gstrCA=&txtCodigo="+stock+"&intIdiomaXsl=0'"
      r = y.execute(q)
    
      if len(r.rows)>0:
        preco = r.rows[0]
        erro = "0"
      elif len(r.rows)<=0:
        preco = "0"
        erro = "1"
    
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
