<%include file="../header.mako" args="pageTitle='User Manager'" />
  <link href="../css/main.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <%include file="../navbars/navbar.mako" args="currentPage='manager'"/>

    <div class="container">

      <table class="table table-striped">
      <thead>
        <tr>
          <th>ID</th>
          <th>Username</th>
          <th>Class</th>
          <th>Date Registered</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>1</td>
          <td>user1</td>
          <td>Admin</td>
          <td>test</td>
        </tr>
        <tr>
          <td>2</td>
          <td>user2</td>
          <td>User</td>
          <td>test</td>
        </tr>
        <tr>
          <td>3</td>
          <td>user3</td>
          <td>Doctor</td>
          <td>test</td>
        </tr>
      </tbody>
      </table>

    </div>

<%include file="../footer.mako"/>