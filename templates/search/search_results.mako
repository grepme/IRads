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

    <div class="container">

    <h2>Search Module <small>Results:</small></h2>
    <table class="table table-striped table-bordered table-hover">
    <thead>
        <tr>
          <th>Patient Name</th>
          <th>Doctor Name</th>
          <th>Radiologist Name</th>
          <th>Test Type</th>
          <th>Prescribing Date</th>
          <th>Test Date</th>
          <th>Diagnosis</th>
          <th>Description</th>
          <th>Images</th>
        </tr>
      </thead>
      <tbody>
      % for result in results:
      <tr>
        <td>${result['patient_name']}</td>
        <td>${result['doctor_name']}</td>
        <td>${result['radiologist_name']}</td>
        <td>${result['test_type']}</td>
        <td>${result['prescribing_date']}</td>
        <td>${result['test_date']}</td>
        <td>${result['diagnosis']}</td>
        <td>${result['description']}</td>
        <td>
        % for image in result['images']:
            <p><a href="/search/viewImage/${image[0]}" target="_blank"><img src="data:image/jpg;base64,${image[1]}" /></a></p>
        % endfor
        </td>
      </tr>
      % endfor
      </tbody>
    </table>
    </div>



<%include file="/footer.mako"/>
