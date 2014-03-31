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
      <h2>Analysis Module <small>Enter criteria:</small></h2>
      <form role="form" action="/analysis/generate" method="POST">
		<label for="datepicker">Date range</label>
        <div class="input-daterange input-group form-group" id="datepicker">
          <input type="text" class="input-sm form-control" name="start" placeholder="YYYY-MM-DD" data-provide="datepicker" data-date-format="yyyy-mm-dd" data-date-today-btn="true" data-date-autoclose="true" data-date-today-highlight="true"/>
          <span class="input-group-addon">to</span>
          <input type="text" class="input-sm form-control" name="end" placeholder="YYYY-MM-DD" data-provide="datepicker" data-date-format="yyyy-mm-dd" data-date-today-btn="true" data-date-autoclose="true" data-date-today-highlight="true"/>
		      <span class="input-group-addon small">(if blank, will search all records)</span>
        </div>
        <div class="form-group">
          <label for="patient">Test Type</label>
          <select name="testType" class="form-control">
		    <option value="_ALLTESTTYPES_">All Test Types</option>
          % for test_type in testTypes:
            <option value="${test_type}">${test_type}</option>
          % endfor
          </select>
        </div>
        <div class="form-group">
          <label for="patient">Patient</label>
          <select name="patient" class="form-control">
		    <option value="_ALLPATIENTS_">All Patients</option>
          % for patient in patients:
            <option value="${patient['person_id']}">${patient['last_name']}, ${patient['first_name']}</option>
          % endfor
          </select>
        </div>
        <button class="btn btn-lg btn-primary btn-block btn-add" type="submit">Generate</button>
        % if action == "noparams":
        <p class="lead">Please fill out all fields.</p>
        % elif action == "fail":
        <p class="lead">No results found.</p>
        % endif
      </form>
    </div>
  </div>
<%include file="/footer.mako"/>
