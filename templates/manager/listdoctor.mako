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

    <h2>User Module <small>Select a doctor:</small></h2>
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
      % for doctor in doctors:
      <tr>
        <td><a href="/manager/editPerson/${doctor['person_id']}">${doctor['last_name']}</a></td>
        <td><a href="/manager/editPerson/${doctor['person_id']}">${doctor['first_name']}</a></td>
        <td><a href="/manager/editPerson/${doctor['person_id']}">${doctor['address']}</a></td>
        <td><a href="/manager/editPerson/${doctor['person_id']}">${doctor['email']}</a></td>
        <td><a href="/manager/editPerson/${doctor['person_id']}">${doctor['phone']}</a></td>
      </tr>
      % endfor
      </tbody>
    </table>
    </div>



<%include file="/footer.mako"/>