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
      <h2>Uploading Module <small>Upload an image:</small></h2>
      <form class="form-upload" role="form" action="/upload/postImage/${id}" method="POST" enctype="multipart/form-data">
        <h2 class="form-upload-heading">Choose a file:</h2>
        <input type="file" name="radiologyimage">
        <p class="help-block">Choose an image file to upload.</p>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Upload</button>
      </form>
    </div>
  </div>
<%include file="/footer.mako"/>
