<%include file="/header.mako" args="pageTitle='User Manager'" />
  <link href="/css/main.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <%include file="/navbars/navbar.mako" args="currentPage='manager'"/>

    <div class="container content">

      <h2>User Module <small>Add a person:</small></h2>

      <form role="form" class="form-add" action="addPerson" method="POST">
        <div class="form-group">
          <label for="firstname">First name</label>
          <input type="text" class="form-control" name="firstname" maxlength="24" placeholder="Enter first name (max 24 characters)" required autofocus>
        </div>
        <div class="form-group">
          <label for="lastname">Last name</label>
          <input type="text" class="form-control" name="lastname" maxlength="24" placeholder="Enter last name (max 24 characters)" required>
        </div>
        <div class="form-group">
          <label for="address">Address</label>
          <input type="text" class="form-control" name="address" maxlength="128" placeholder="Enter address (max 128 characters)" required>
        </div>
        <div class="form-group">
          <label for="email">Email Address</label>
          <input type="email" class="form-control" name="email" maxlength="128" placeholder="Enter email address (max 128 characters)" required>
        </div>
        <div class="form-group">
          <label for="phone">Phone number</label>
          <input type="text" class="form-control" name="phone" maxlength="10" placeholder="XXX#######" required>
        </div>
        <button class="btn btn-lg btn-primary btn-block btn-add" type="submit">Add</button>
          % if action:
      <p class="lead">Person successfully added.</p>
          % endif
    </form>
    </div>



<%include file="/footer.mako"/>