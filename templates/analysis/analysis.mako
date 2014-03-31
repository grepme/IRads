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
        <div class="btn-group" data-toggle="buttons">
         <label class="btn btn-primary">
           <input type="radio" name="options" id="option1" value="week"> Week
         </label>
         <label class="btn btn-primary">
           <input type="radio" name="options" id="option2" value="month"> Month
         </label>
         <label class="btn btn-primary">
           <input type="radio" name="options" id="option3" value="year"> Year
         </label>
         <label class="btn btn-primary">
           <input type="radio" name="options" id="option3" value="all"> All Time
         </label>
       </div>
       <div class="form-group">
          <label for="keywords">Test Type</label>
          <input type="text" class="form-control" name="keywords" placeholder="Enter test type" />
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
