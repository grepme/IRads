<%include file="/header.mako" args="pageTitle='Data Analysis'" />
  <link href="/css/main.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <%include file="/navbars/navbar.mako" args="currentPage='analysis'"/>
 <div class="container content">
      <h2>Analysis Module <small>Results</small></h2>
	  ${results}
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>Patient's Name</th>
            % for test in testTypes:
			  <th>${test}</th>
			% endfor
          </tr>
        </thead>
       <tbody>
	   % for result in results:
        <tr>
          <td>${result[0].patient.last_name}, ${result[0].patient.first_name}</td>
        </tr>
		% endfor
      </tbody>
      </table>
	  ${str(results)}
    </div>
  </div>
<%include file="/footer.mako"/>
