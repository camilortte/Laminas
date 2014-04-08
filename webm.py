import web
import lxml.html
from lxml.cssselect import CSSSelector
import pdfkit


PAGINA='http://www.laneros.com/mis-laminas/365521/'

def getPDF(user):
	tree = lxml.html.parse(user)

	album=[0]*640

	latengoCSS = CSSSelector('.laTengo')
	repetidaCSS = CSSSelector('.repetida')


	tableText=""


	results = latengoCSS(tree)
	for  result in results:
		#print dir(result)
		album[int(result.text)]=1
		#print lxml.html.tostring(result).strip()

	results = repetidaCSS(tree)
	for  result in results:
		album[int(result.text)]=2


	tableText="<table>\n<tr>"
	contador=0
	for elemento in album:
		calificativo=""
		if contador%20==0 and contador!=0:
			tableText+="</tr>"
			tableText+="<tr>"				
				
		if(elemento==1):
			calificativo="TENGO"
		else:
			if (elemento==2):
				calificativo="REPETIDO"
			else:
				calificativo="NONE"

		tableText+="<td class='"+calificativo+"'>"+str(contador)+"</td>"
		#print contador
		contador+=1

	tableText+="</tr></table>"

	css="<style> .TENGO {background-color:green;} .REPETIDO {background-color:red;} .NONE {background-color:white;} table{margin:auto;border:0.5em}</style>\n"
	#print css+tableText
	return pdfkit.from_string(css+tableText+"<br> <h1>Created by @camilortte</h1>", 'static/outs.pdf')
	#pdfkit.from_url('http://google.com', 'out.pdf')

urls = (
'/', 'index'
)

app = web.application(urls, globals())

class index:
	def GET(self):
	  return """
	  <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
	  <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es" lang="es">
	  <head>
	  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	      <title>Generador PDF Laminitas</title>
	      <style type="text/css" media="screen">
	        h1 {text-align:center; color: #444;}
	        form {text-align:center; color: #444; margin:auto}
	        .inp {width:50%}
	      </style>
	  </head>
	  <body>
	    <h1>Ingresa el link de la pagina: <br>Ejemplo: http://www.laneros.com/mis-laminas/365521/</h1>
	    <form name='form' method="post">
			<input class='inp' type="input" name='user'/>
			<input type="submit"/>
	    </form>
	  </body>
	  </html>
	  """

	def POST(self):
		try:
			form =  web.input()      			      	
			getPDF(form.user)
		except  Exception,e:
			return """
	  <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
	  <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es" lang="es">
	  <head>
	  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	      <title>Generador PDF Laminitas</title>
	      <style type="text/css" media="screen">
	        h1 {text-align:center: color: #444;}
	        form {text-align:center; color: #444; margin:auto}
	        .inp {width:50%}
	      </style>
	  </head>
	  <body>
	    <h1>Ingresa el link de la pagina; <br>Ejemplo: http://www.laneros.com/mis-laminas/365521/</h1>
	    <form name='form' method="post">
			<input class='inp' type="input" name='user'/>
			<input type="submit"/>
	    </form>
	    <h1>Error Lo que Ingresaste no es valido</h1>
	  </body>
	  </html>
	  """+str(e)
		return  web.seeother("/static/outs.pdf")
	
if __name__ == '__main__':
	app.run()