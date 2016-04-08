#!/usr/bin/python



import webapp
import urllib2

class CacheApp (webapp.webApp):

    diccNav2App = {}
    diccSer2App = {}
    diccApp2Nav = {}

    contadorNav2App = 0
    contadorSer2App = 0
    contadorApp2Nav = 0

    def parse(self, request):
        self.diccNav2App[self.contadorNav2App] = request
        self.contadorNav2App = self.contadorNav2App + 1

        try:
        	resource = request.split(' ', 2)[1][1:] # quita tambien la barra
        except IndexError:
        	resource = ''

        return resource

    def process(self, resource):

        # Compruebo si es una redireccion, ya que si lo es tengo que hacer el mismo procedimiento
        # que si no lo es excepto el primer paso.
        # Por eso saco el primer paso (quedarme con la pagina que piden) al principio para
        # dejar el resto de pasos en comun y ahorrar codigo.
        try:
            recurso = resource.split('/')[0]
            print "LO PARTOOOOOOO"
            if recurso == "reload":
                resource = resource.split('/')[1]
                print "LO RECARGOOOOOOO"
        except IndexError:
			pass

        url = 'http://' + resource
        print "CREO URL!!!!"

        if resource == "CabecerasNav2App":
            httpCode = "200 Ok"
            htmlBody = str(self.diccNav2App.items())
        elif resource == "CabecerasApp2Nav":
            httpCode = "200 Ok"
            htmlBody = str(self.diccApp2Nav.items())
        elif resource == "CabecerasServ2App":
            httpCode = "200 Ok"
            htmlBody = str(self.diccSer2App.items())
        else:

            try:
                pagina = urllib2.urlopen(url)
                self.diccSer2App[self.contadorSer2App] = pagina.info().headers
                self.contadorSer2App = self.contadorSer2App + 1
                cuerpo = pagina.read()
                punto1 = cuerpo.find("<body")
                punto2 = cuerpo.find(">", punto1)
                enlaces = "<a href=" + url + "> Original Webpage </a>" \
                        + "<a href=/reload/" + resource + "> Refresh </a>" \
                        + "<a href=/CabecerasNav2App> Client-to-App-Side HTTP </a>" \
                        + "<a href=/CabecerasApp2Nav> App-to-Client-Side HTTP </a>" \
                        + "<a href=/CabecerasServ2App> Server-to-App-Side HTTP </a>" \
        				+ "\n" + "</br></br"
                cuerpo = cuerpo[:punto2+1] + enlaces + cuerpo[punto2+1:]

                httpCode = str(pagina.getcode())
                htmlBody = cuerpo
            except:
                htmlBody = "Could not connect"
                httpCode = "404 Not Found"
            self.diccApp2Nav[self.contadorApp2Nav] = httpCode
            self.contadorApp2Nav = self.contadorApp2Nav + 1

        print "el contador de App2Nav va -> " + str(self.contadorApp2Nav) + "\n"
        print "el contador de Nav2App va -> " + str(self.contadorNav2App) + "\n"
        print "el contador de Ser2App va -> " + str(self.contadorSer2App) + "\n"

        return (httpCode, htmlBody)

if __name__=="__main__":
	testCacheApp = CacheApp("localhost", 1235)
