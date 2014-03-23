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
    </div>
  </div>
<%include file="/footer.mako"/>