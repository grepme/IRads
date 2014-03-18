import cherrpy
def protect(groups=None, redirect=True):
	results = getAllUserData(cherrypy.session.get('session_id'))
	if results:
		if results['username'] != cherrypy.session.get('username'):
			cherrypy.session.delete()
			cherrypy.session['redirect'] = cherrypy.request.path_info
			raise cherrypy.HTTPRedirect("/")
		if groups:
			allowed = False
			for x in groups:
				if results['group'] == x:
					allowed = True
			if not allowed:
				raise cherrypy.HTTPError("403 Forbidden", "You are not allowed to access this resource.")
	else:
		cherrypy.session.delete()
		cherrypy.session['redirect'] = cherrypy.request.path_info
		raise cherrypy.HTTPRedirect("/")

cherrypy.tools.protect = cherrypy.Tool('before_handler', protect)