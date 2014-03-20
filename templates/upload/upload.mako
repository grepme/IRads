<%include file="../header.mako" args="pageTitle='Upload'" />
  <link href="../css/upload.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <%include file="../navbars/navbar.mako" args="currentPage='upload'"/>
    <div class="container">
    % if action == 'imageUpload':
    <h2>Uploading Module <small>Upload an image:</small></h2>
      <form class="form-upload" role="form">
        <h2 class="form-upload-heading">Choose a file:</h2>
        <input type="file" id="radiologyimage">
        <p class="help-block">Choose a .jpg file to upload.</p>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Upload</button>
      </form>
    % elif action == 'imageSelect':
    <h2>Uploading Module <small>Select a record:</small></h2>
    % elif action == 'addRecord':
    <h2>Uploading Module <small>Add a record:</small></h2>
      <form class="form-add" role="form">
        <div class="form-group">
          <label for="patient">Patient</label>
          <select id="patient" class="form-control">
          % for patient in patients:
            <option value="${patient[0]}">${patient[0]}. ${patient[1]}</option>
          % endfor
          </select>
        </div>
        <div class="form-group">
          <label for="doctor">Doctor</label>
          <select id="doctor" class="form-control">
          % for doctor in doctors:
            <option value="${doctor[0]}">${doctor[0]}. ${doctor[1]}</option>
          % endfor
          </select>
        </div>
        <div class="form-group">
          <label for="test_type">Test type</label>
          <input type="text" class="form-control" id="test_type" maxlength="24" placeholder="Enter test type (max 24 characters)">
        </div>
        <div class="form-group">
          <label for="test_date">Test date</label>
          <input type="text" class="form-control" id="test_date" maxlength="10" placeholder="YYYY-MM-DD">
        </div>
        <div class="form-group">
          <label for="prescribing_date">Prescribing date</label>
          <input type="text" class="form-control" id="prescribing_date" maxlength="10" placeholder="YYYY-MM-DD">
        </div>
        <div class="form-group">
          <label for="diagnosis">Diagnosis</label>
          <textarea class="form-control" rows="3" id="diagnosis" maxlength="128" placeholder="Enter diagnosis (max 128 characters)"></textarea>
        </div>
        <div class="form-group">
          <label for="description">Description</label>
          <textarea class="form-control" rows="10" id="test_type" maxlength="1024" placeholder="Enter description (max 1024 characters)"></textarea>
        </div>
        <button class="btn btn-lg btn-primary btn-block btn-add" type="submit">Add</button>
      </form>
    % else:
    <h2>Uploading Module <small>Select an action:</small></h2>
    <p><a href="/upload/addRecord">Add a new record</a></p>
    <p><a href="/upload/imageSelect">Add images to an existing record</a></p>
    % endif
    </div>
    </div>

<%include file="../footer.mako"/>