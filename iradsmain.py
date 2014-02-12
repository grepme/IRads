import cherrypy


class Irads(object):
    #This will expose the object to the web.
    # ie. Think public vs. private definitions.
    @cherrypy.expose
    def index(self):
        return "Hello World! This is the start of the project!"
    
    #This will map the definition to '/page1'
    @cherrypy.expose
    def page1(self):
      return "This is a side page"
      
    #This will map the definition to '/page2/[variable1]'
    #[variable 1 being the first variable]
    @cherrypy.expose
    def page2(self, var):
      return "You sent me the variable!: " + str(var)
      
class Something(object):
  @cherrypy.expose
  def index():
    return "This should probably have an index..."

#This will map the object to '/'
Mapping = Irads()

#I can map the class to '/somethingelse' instead!
Mapping.somethingelse = Something()

#Plug it into the quickstart with the default config.
cherrypy.quickstart(Mapping)
