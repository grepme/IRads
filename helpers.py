#Helper functions

import cherrypy


def getUserInfo():
    """Returns the username and class of the current
    session's user
    """
    return (cherrypy.session.get('username'), cherrypy.session.get('classtype'))


def protect(groups=None, redirect=True):
    """Checks login credentials and restricts access to
    secure pages to logged in users with appropriate access only
    """
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

'''
Register protect as a CherryPy handler
so we can use it as a decorator
eg.
@cherrypy.tools.protect(groups=['a'])
'''
cherrypy.tools.protect = cherrypy.Tool('before_handler', protect)
