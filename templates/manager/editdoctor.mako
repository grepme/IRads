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

    <h2>User Module <small>Edit patients:</small></h2>
    % if patients:
    <table class="table table-striped table-bordered table-hover">
    <thead>
        <tr>
          <th>Last Name</th>
          <th>First Name</th>
          <th>Address</th>
          <th>Email</th>
          <th>Phone</th>
          <th>Remove</th>
        </tr>
      </thead>
      <tbody>
      % for patient in patients:
      <tr>
        <td>${patient['last_name']}</a></td>
        <td>${patient['first_name']}</a></td>
        <td>${patient['address']}</a></td>
        <td>${patient['email']}</a></td>
        <td>${patient['phone']}</a></td>
        <td><a href="/manager/editDoctor/${doctor}/remove/${patient['person_id']}">Remove</a></td>
      </tr>
      % endfor
      </tbody>
    </table>
    % endif
    <form class="form-add" role="form" action="/manager/editDoctor/${doctor}" method="POST">
        <div class="form-group">
          <label for="addId">Person</label>
          <select name="addId" class="form-control">
          % for person in people:
            <option value="${person['person_id']}">${person['last_name']}, ${person['first_name']}</option>
          % endfor
          </select>
        </div>
        <button class="btn btn-lg btn-primary btn-block btn-add" type="submit">Add</button>
    </div>
  </div>

<%include file="/footer.mako"/>