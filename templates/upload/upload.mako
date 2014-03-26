<%include file="/header.mako" args="pageTitle='Upload'" />
  <link href="/css/main.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <%include file="/navbars/navbar.mako" args="currentPage='upload'"/>
    <div class="container content">
      <h2>Uploading Module <small>Select an action:</small></h2>
      <h5><a href="/upload/addRecord">Add a new record</a></h5>
      <h5><a href="/upload/selectRecord">Add images to an existing record</a></h5>
      % if action == 'noPatient':
      <p class="lead">No patients found. Cannot add record.</p>
      % elif action == 'noDoctor':
      <p class="lead">No doctors found. Cannot add record.</p>
      % elif action == 'success':
      <p class="lead">Record added successfully.</p>
      % elif action == 'added':
      <p class="lead">Image added successfully.</p>
      % elif action == 'error':
      <p class="lead">An error occurred.</p>
      % endif
    </div>
  </div>
<%include file="/footer.mako"/>
