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

      <h2>User Module <small>Edit user:</small></h2>
      <h4>All fields are optional. Fields with content will be changed.</h4>

      <form role="form" class="form-add" action="/manager/editUser/${user['user_name']}" method="POST">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" class="form-control" name="username" maxlength="24" placeholder="${user['user_name']}" autofocus>
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" class="form-control" name="password" maxlength="24" placeholder="Enter new password (max 24 characters)">
        </div>
        <div class="form-group">
          <label for="password2">Repeat password</label>
          <input type="password" class="form-control" name="password2" maxlength="24" placeholder="Enter new password (max 24 characters)">
        </div>
        <div class="form-group">
          <label for="classtype">Access class</label>
          <select name="classtype" class="form-control" required>
            % if user['class_type'] == 'a':
            <option value="a" selected>Administrator</option>
            <option value="d">Doctor</option>
            <option value="p">Patient</option>
            <option value="r">Radiologist</option>
            % elif user['class_type'] == 'd':
            <option value="a">Administrator</option>
            <option value="d" selected>Doctor</option>
            <option value="p">Patient</option>
            <option value="r">Radiologist</option>
            % elif user['class_type'] == 'p':
            <option value="a">Administrator</option>
            <option value="d">Doctor</option>
            <option value="p" selected>Patient</option>
            <option value="r">Radiologist</option>
            % elif user['class_type'] == 'r':
            <option value="a">Administrator</option>
            <option value="d">Doctor</option>
            <option value="p">Patient</option>
            <option value="r" selected>Radiologist</option>
            % endif
          </select>
        </div>
        <button class="btn btn-lg btn-primary btn-block btn-add" type="submit">Edit</button>
          % if action == "success":
      <p class="lead">User successfully edited.</p>
          % elif action == "nomatch":
      <p class="lead">An error occurred: The passwords did not match.</p>
          % endif
    </form>
    </div>
<%include file="/footer.mako"/>