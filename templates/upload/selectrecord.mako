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
      <h2>Uploading Module <small>Select a record:</small></h2>
      <table class="table table-striped table-bordered table-hover">
        <thead>
          <tr>
            <th>Prescribing Date</th>
            <th>Testing&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; date</th>
            <th>Diagnosis&nbsp;&nbsp;&nbsp;&nbsp;</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
        % for record in records:
          <tr>
            <td><a href="/upload/selectImage/${record[0]}">${record[1]}</a></td>
            <td><a href="/upload/selectImage/${record[0]}">${record[2]}</a></td>
            <td><a href="/upload/selectImage/${record[0]}">${record[3]}</a></td>
            <td><a href="/upload/selectImage/${record[0]}">${record[4]}</a></td>
          </tr>
        % endfor
        </tbody>
      </table>
    </div>
  </div>
<%include file="/footer.mako"/>
