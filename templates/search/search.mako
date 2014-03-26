<%include file="/header.mako" args="pageTitle='Search'" />
  <link href="/css/main.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <%include file="/navbars/navbar.mako" args="currentPage='search'"/>
    <div class="container content">
      <h2>Search Module <small>Enter criteria:</small></h2>
      <form role="form" action="/search/search" method="POST">
        <label for="datepicker">Date range</label>
        <div class="input-daterange input-group form-group" id="datepicker">
          <input type="text" class="input-sm form-control" name="start" data-provide="datepicker" data-date-format="yyyy-mm-dd" data-date-today-btn="true" data-date-autoclose="true" data-date-today-highlight="true" required/>
          <span class="input-group-addon">to</span>
          <input type="text" class="input-sm form-control" name="end" data-provide="datepicker" data-date-format="yyyy-mm-dd" data-date-today-btn="true" data-date-autoclose="true" data-date-today-highlight="true" required/>
        </div>
        <div class="form-group">
          <label for="keywords">Keyword(s)</label>
          <input type="text" class="form-control" name="keywords" placeholder="Enter keyword(s)" required>
        </div>
        <div class="radio">
          <label>
            <input type="radio" name="sort" id="sortdatenewest" value="newest" checked>
            Sort by most-recent-first
          </label>
        </div>
        <div class="radio">
          <label>
            <input type="radio" name="sort" id="sortdateoldest" value="oldest">
            Sort by least-recent-first
          </label>
        </div>
        <div class="radio">
          <label>
            <input type="radio" name="sort" id="sortscore" value="score">
            Sort by score
          </label>
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
