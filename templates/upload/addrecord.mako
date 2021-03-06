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
      <h2>Uploading Module <small>Add a record:</small></h2>
      <form class="form-add" role="form" action="postRecord" method="POST">
        <div class="form-group">
          <label for="patient">Patient</label>
          <select name="patient" class="form-control">
          % for patient in patients:
            <option value="${patient['person_id']}">${patient['last_name']}, ${patient['first_name']}</option>
          % endfor
          </select>
        </div>
        <div class="form-group">
          <label for="doctor">Doctor</label>
          <select name="doctor" class="form-control">
          % for doctor in doctors:
            <option value="${doctor['person_id']}">${doctor['last_name']}, ${doctor['first_name']}</option>
          % endfor
          </select>
        </div>
        <div class="form-group">
          <label for="test_type">Test type</label>
          <input type="text" class="form-control" name="test_type" maxlength="24" placeholder="Enter test type (max 24 characters)" required>
        </div>
        <div class="form-group">
          <label for="test_date">Test date</label>
          <input type="text" class="form-control" name="test_date" maxlength="10" placeholder="YYYY-MM-DD" data-provide="datepicker" data-date-format="yyyy-mm-dd" data-date-today-btn="true" data-date-autoclose="true" data-date-today-highlight="true" required>
        </div>
        <div class="form-group">
          <label for="prescribing_date">Prescribing date</label>
          <input type="text" class="form-control" name="prescribing_date" maxlength="10" placeholder="YYYY-MM-DD" data-provide="datepicker" data-date-format="yyyy-mm-dd" data-date-today-btn="true" data-date-autoclose="true" data-date-today-highlight="true" required>
        </div>
        <div class="form-group">
          <label for="diagnosis">Diagnosis</label>
          <textarea class="form-control" rows="3" name="diagnosis" maxlength="128" placeholder="Enter diagnosis (max 128 characters)" required></textarea>
        </div>
        <div class="form-group">
          <label for="description">Description</label>
          <textarea class="form-control" rows="10" name="description" maxlength="1024" placeholder="Enter description (max 1024 characters)" required></textarea>
        </div>
        <button class="btn btn-lg btn-primary btn-block btn-add" type="submit">Add</button>
      </form>
    </div>
  </div>
<%include file="/footer.mako"/>
