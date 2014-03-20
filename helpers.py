import cherrypy


def getUserInfo():
    return (cherrypy.session.get('username'), cherrypy.session.get('classtype'))


def protect(groups=None, redirect=True):
    username = cherrypy.session.get('username')
    classtype = cherrypy.session.get('classtype')
    if username:
        if groups:
            allowed = False
            for x in groups:
                if classtype == x:
                    allowed = True
            if not allowed:
                raise cherrypy.HTTPError(
                    403, "You are not allowed to access this resource.")
    else:
        cherrypy.session['redirect'] = cherrypy.request.path_info
        raise cherrypy.HTTPRedirect("/error")

cherrypy.tools.protect = cherrypy.Tool('before_handler', protect)
