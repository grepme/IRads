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

    <h2>User Module <small>Select a person:</small></h2>
    <table class="table table-striped table-bordered table-hover">
    <thead>
        <tr>
          <th>Last Name</th>
          <th>First Name</th>
          <th>Address</th>
          <th>Email</th>
          <th>Phone</th>
        </tr>
      </thead>
      <tbody>
      % for person in persons:
      <tr>
        <td><a href="/manager/editPerson/${person['person_id']}">${person['last_name']}</a></td>
        <td><a href="/manager/editPerson/${person['person_id']}">${person['first_name']}</a></td>
        <td><a href="/manager/editPerson/${person['person_id']}">${person['address']}</a></td>
        <td><a href="/manager/editPerson/${person['person_id']}">${person['email']}</a></td>
        <td><a href="/manager/editPerson/${person['person_id']}">${person['phone']}</a></td>
      </tr>
      % endfor
      </tbody>
    </table>
    </div>



<%include file="/footer.mako"/>