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

      <h2>User Module <small>Edit person:</small></h2>
      <h4>All fields are optional. Fields with content will be changed.</h4>

      <form role="form" class="form-add" action="/manager/editPerson/${person['person_id']}" method="POST">
        <div class="form-group">
          <label for="firstname">First name</label>
          <input type="text" class="form-control" name="firstname" maxlength="24" placeholder="${person['first_name']}" autofocus>
        </div>
        <div class="form-group">
          <label for="lastname">Last name</label>
          <input type="text" class="form-control" name="lastname" maxlength="24" placeholder="${person['last_name']}">
        </div>
        <div class="form-group">
          <label for="address">Address</label>
          <input type="text" class="form-control" name="address" maxlength="128" placeholder="${person['address']}">
        </div>
        <div class="form-group">
          <label for="email">Email Address</label>
          <input type="email" class="form-control" name="email" maxlength="128" placeholder="${person['email']}">
        </div>
        <div class="form-group">
          <label for="phone">Phone number</label>
          <input type="text" class="form-control" name="phone" maxlength="10" placeholder="${person['phone']}">
        </div>
        <button class="btn btn-lg btn-primary btn-block btn-add" type="submit">Edit</button>
          % if action:
      <p class="lead">Person successfully edited.</p>
          % endif
    </form>
     <h5><a href="/manager/addUser/${person['person_id']}">Add a username for this person</a></h5>
    </div>



<%include file="/footer.mako"/>