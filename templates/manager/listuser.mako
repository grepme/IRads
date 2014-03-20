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

    <h2>User Module <small>Select a user:</small></h2>
    <table class="table table-striped table-bordered table-hover">
    <thead>
        <tr>
          <th>Username</th>
          <th>Access class</th>
          <th>Date Registered</th>
        </tr>
      </thead>
      <tbody>
      % for user in users:
      <tr>
        <td><a href="/manager/editUser/${user['user_name']}">${user['user_name']}</a></td>
        % if user['class_type'] == 'a':
        <td><a href="/manager/editUser/${user['user_name']}">Administrator</a></td>
        % elif user['class_type'] == 'd':
        <td><a href="/manager/editUser/${user['user_name']}">Doctor</a></td>
        % elif user['class_type'] == 'p':
        <td><a href="/manager/editUser/${user['user_name']}">Patient</a></td>
        % elif user['class_type'] == 'r':
        <td><a href="/manager/editUser/${user['user_name']}">Radiologist</a></td>
        % endif
        <td><a href="/manager/editUser/${user['user_name']}">${user['date_registered']}</a></td>
      </tr>
      % endfor
      </tbody>
    </table>
    </div>



<%include file="/footer.mako"/>