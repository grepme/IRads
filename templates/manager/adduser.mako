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

      <h2>User Module <small>Add a user:</small></h2>

      <form role="form" class="form-add" action="addUser" method="POST">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="username" class="form-control" name="username" maxlength="24" placeholder="Enter username (max 24 characters)" required autofocus>
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" class="form-control" name="password" maxlength="24" placeholder="Enter password (max 24 characters)" required>
        </div>
        <div class="form-group">
          <label for="classtype">Access class</label>
          <select name="classtype" class="form-control" required>
            <option value="a">Administrator</option>
            <option value="d">Doctor</option>
            <option value="p">Patient</option>
            <option value="r">Radiologist</option>
          </select>
        </div>
        <div class="form-group">
          <label for="id">Username assigned to:</label>
          <select name="id" class="form-control" required>
          % for person in persons:
            <option value="${person[0]}">${person[2]}, ${person[1]}</option>
          % endfor
          </select>
        </div>
        <button class="btn btn-lg btn-primary btn-block btn-add" type="submit">Add</button>
          % if action:
      <p class="lead">User successfully added.</p>
          % endif
    </form>
    </div>



<%include file="/footer.mako"/>