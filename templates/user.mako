<%include file="header.mako" args="pageTitle='Change Password'" />

  <link href="css/main.css" rel="stylesheet">
  <link href="css/login.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <%include file="navbars/navbar.mako" args="currentPage='user'"/>

    <div class="container">
    <form class="form-signin" role="form" action="user" method="POST">
        <h2 class="form-signin-heading">Change passsword</h2>
        <label for="password">Password</label>
        <input type="password" name="password" class="form-control" placeholder="New password" maxlength="24" required autofocus>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Change</button>
      </form>
      % if action:
    <p class="lead">Your password was changed.</p>
      % endif
    </div>


<%include file="footer.mako"/>