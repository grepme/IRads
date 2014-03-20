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

    <div class="container">

      <h2>User Module <small>Select an action:</small></h2>
      <p><a href="/manager/addPerson">Add a person</a></p>
      <p><a href="/manager/listPerson">View persons and edit details</a></p>
      <p><a href="/manager/addUser">Add a username for a person</a></p>
      <p><a href="/manager/listUser">View usernames and edit details</a></p>
      <p><a href="/manager/listDoctor">View and edit doctors' patients</a></p>

    </div>

<%include file="/footer.mako"/>