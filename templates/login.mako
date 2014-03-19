<%include file="header.mako" args="pageTitle='Login'" />

<link href="css/login.css" rel="stylesheet">
</head>
 <body>

    <div class="container">
	 
      <form class="form-signin" role="form" action="checkLogin" method="POST">
        <h2 class="form-signin-heading">IRads: Please sign in</h2>
        <input type="username" name="username" class="form-control" placeholder="Username" maxlength="24" required autofocus>
        <input type="password" name="password" class="form-control" placeholder="Password" maxlength="24" required>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
      </form>
      % if loginStatus==1:
	<p class="lead">Invalid login! Please try again.</p>
	  % elif loginStatus==2:
	<p class="lead">You have been logged out.</p>
	  % endif
    </div>

<%include file="footer.mako"/>