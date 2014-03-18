<%include file="header.mako" args="pageTitle='Login'" />

<link href="css/login.css" rel="stylesheet">
</head>
 <body>

    <div class="container">

      <form class="form-signin" role="form">
        <h2 class="form-signin-heading">Please sign in</h2>
        <input type="username" class="form-control" placeholder="Username" required autofocus>
        <input type="password" class="form-control" placeholder="Password" required>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
      </form>

    </div>

<%include file="footer.mako"/>