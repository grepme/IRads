<%include file="/header.mako" args="pageTitle='User Manager'" />
  <link href="/css/main.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <%include file="/navbars/navbar.mako" args="currentPage='report'"/>

    <div class="container content">

    <h2>Report Module <small>Results:</small></h2>
    <table class="table table-striped table-bordered table-hover">
    <thead>
        <tr>
          <th>Last Name</th>
          <th>First Name</th>
          <th>Address</th>
          <th>Phone</th>
          <th>Test Date</th>
          <th>Diagnosis</th>
        </tr>
      </thead>
      <tbody>
      % for result in results:
      <tr>
        <td>${result[0]}</td>
        <td>${result[1]}</td>
        <td>${result[2]}</td>
        <td>${result[3]}</td>
        <td>${result[4]}</td>
        <td>${result[5]}</td>
      </tr>
      % endfor
      </tbody>
    </table>
    </div>



<%include file="/footer.mako"/>
