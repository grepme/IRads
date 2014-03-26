<%include file="/header.mako" args="pageTitle='Report Generator'" />
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
      <h2>Report Module <small>Enter criteria:</small></h2>
      <form role="form" action="/report/search" method="POST">
        <label for="datepicker">Date range</label>
        <div class="input-daterange input-group form-group" id="datepicker">
          <input type="text" class="input-sm form-control" name="start" placeholder="YYYY-MM-DD" data-provide="datepicker" data-date-format="yyyy-mm-dd" data-date-today-btn="true" data-date-autoclose="true" data-date-today-highlight="true" required/>
          <span class="input-group-addon">to</span>
          <input type="text" class="input-sm form-control" name="end" placeholder="YYYY-MM-DD" data-provide="datepicker" data-date-format="yyyy-mm-dd" data-date-today-btn="true" data-date-autoclose="true" data-date-today-highlight="true" required/>
        </div>
        <div class="form-group">
          <label for="diagnosis">Diagnosis</label>
          <input type="text" class="form-control" name="diagnosis" placeholder="Enter keyword(s)" required>
        </div>
        <button class="btn btn-lg btn-primary btn-block btn-add" type="submit">Search</button>
        % if action == "noparams":
        <p class="lead">Please fill out all fields.</p>
        % elif action == "fail":
        <p class="lead">No results found.</p>
        % endif
      </form>
    </div>
  </div>
<%include file="/footer.mako"/>
