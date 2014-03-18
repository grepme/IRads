<%include file="../header.mako" args="pageTitle='Upload'" />
  <link href="../css/upload.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <%include file="../navbars/admin.mako" args="currentPage='upload'"/>

    <div class="container">

      <form class="form-upload" role="form">
        <h2 class="form-upload-heading">Choose a file:</h2>
        <input type="file" id="radiologyimage">
        <p class="help-block">Choose a .jpg file to upload.</p>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Upload</button>
      </form>

    </div>
    </div>

<%include file="../footer.mako"/>