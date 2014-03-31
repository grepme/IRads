<%include file="/header.mako" args="pageTitle='User Manager'" />
  <link href="/css/main.css" rel="stylesheet">
  </head>

  <body>

    <%include file="/navbars/navbar.mako" args="currentPage='manager'"/>

    <div class="container content">

      <h2>User Module <small>Edit user:</small></h2>
      <h4>All fields are optional. Fields with content will be changed.</h4>
      <form role="form" class="form-add" action="/manager/editUser/${user['user_name']}" method="POST">
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" class="form-control" name="password" maxlength="24" placeholder="Enter new password (max 24 characters)">
        </div>
        <div class="form-group">
          <label for="password2">Repeat password</label>
          <input type="password" class="form-control" name="password2" maxlength="24" placeholder="Enter new password (max 24 characters)">
        </div>

        <div class="form-group">
          <button class="btn btn-lg btn-primary btn-block btn-add" type="submit">Edit</button>
        </div>

          % if action == "success":
        <p class="lead">User successfully edited.</p>
          % elif action == "nomatch":
        <p class="lead">An error occurred: The passwords did not match.</p>
          % endif
      </form>
    </div>
<%include file="/footer.mako"/>
