<%include file="header.mako" args="pageTitle='Change Password'" />

  <link href="css/main.css" rel="stylesheet">
  <link href="css/user.css" rel="stylesheet">

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
        <h2 class="form-signin-heading">Edit Details</h2>
        <h4>All fields are optional. Fields with content will be changed.</h4>
        <div class="form-group">
          <label for="firstname">First name</label>
          <input type="text" class="form-control" name="firstname" maxlength="24" placeholder="${oldinfo[0]}" autofocus>
        </div>
        <div class="form-group">
          <label for="lastname">Last name</label>
          <input type="text" class="form-control" name="lastname" maxlength="24" placeholder="${oldinfo[1]}">
        </div>
        <div class="form-group">
          <label for="address">Address</label>
          <input type="text" class="form-control" name="address" maxlength="128" placeholder="${oldinfo[2]}">
        </div>
        <div class="form-group">
          <label for="email">Email Address</label>
          <input type="email" class="form-control" name="email" maxlength="128" placeholder="${oldinfo[3]}">
        </div>
        <div class="form-group">
          <label for="phone">Phone number</label>
          <input type="text" class="form-control" name="phone" maxlength="10" placeholder="${oldinfo[4]}">
        </div>
        <div class="form-group">
        <label for="password">Password</label>
        <input type="password" name="password" class="form-control" placeholder="New password" maxlength="24">
        </div>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Change</button>
      </form>
      % if action:
    <p class="lead">Your information was changed.</p>
      % endif
    </div>


<%include file="footer.mako"/>