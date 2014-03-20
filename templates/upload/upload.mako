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
    % if action == 'selectImage':
    <h2>Uploading Module <small>Upload an image:</small></h2>
      <form class="form-upload" role="form" action="postImage" method="POST">
        <h2 class="form-upload-heading">Choose a file:</h2>
        <input type="file" name="radiologyimage">
        <p class="help-block">Choose a .jpg file to upload.</p>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Upload</button>
      </form>
    % elif action == 'selectRecord':
    <h2>Uploading Module <small>Select a record:</small></h2>
    <table class="table table-striped table-bordered table-hover">
    <thead>
        <tr>
          <th>#</th>
          <th>Prescribing Date</th>
          <th>Test Date</th>
          <th>Diagnosis</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
      % for record in records:
      <tr>
        <td><a href="/upload/upload/${record[0]}">${record[0]}</a></td>
        <td><a href="/upload/upload/${record[0]}">${record[1]}</a></td>
        <td><a href="/upload/upload/${record[0]}">${record[2]}</a></td>
        <td><a href="/upload/upload/${record[0]}">${record[3]}</a></td>
        <td><a href="/upload/upload/${record[0]}">${record[4]}</a></td>
      </tr>
      % endfor
      </tbody>
    </table>
    % elif action == 'addRecord':
    <h2>Uploading Module <small>Add a record:</small></h2>
      <form class="form-add" role="form" action="postRecord" method="POST">
        <div class="form-group">
          <label for="patient">Patient</label>
          <select name="patient" class="form-control">
          % for patient in patients:
            <option value="${patient[0]}">${patient[0]}. ${patient[1]}</option>
          % endfor
          </select>
        </div>
        <div class="form-group">
          <label for="doctor">Doctor</label>
          <select name="doctor" class="form-control">
          % for doctor in doctors:
            <option value="${doctor[0]}">${doctor[0]}. ${doctor[1]}</option>
          % endfor
          </select>
        </div>
        <div class="form-group">
          <label for="test_type">Test type</label>
          <input type="text" class="form-control" name="test_type" maxlength="24" placeholder="Enter test type (max 24 characters)" required>
        </div>
        <div class="form-group">
          <label for="test_date">Test date</label>
          <input type="text" class="form-control" name="test_date" maxlength="10" placeholder="YYYY-MM-DD" required>
        </div>
        <div class="form-group">
          <label for="prescribing_date">Prescribing date</label>
          <input type="text" class="form-control" name="prescribing_date" maxlength="10" placeholder="YYYY-MM-DD" required>
        </div>
        <div class="form-group">
          <label for="diagnosis">Diagnosis</label>
          <textarea class="form-control" rows="3" name="diagnosis" maxlength="128" placeholder="Enter diagnosis (max 128 characters)" required></textarea>
        </div>
        <div class="form-group">
          <label for="description">Description</label>
          <textarea class="form-control" rows="10" name="test_type" maxlength="1024" placeholder="Enter description (max 1024 characters)" required></textarea>
        </div>
        <button class="btn btn-lg btn-primary btn-block btn-add" type="submit">Add</button>
      </form>
    % else:
    <h2>Uploading Module <small>Select an action:</small></h2>
    <h5><a href="/upload/addRecord">Add a new record</a></h5>
    <h5><a href="/upload/selectRecord">Add images to an existing record</a></h5>
    % endif
    </div>
    </div>

<%include file="/footer.mako"/>