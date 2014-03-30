<%page args="currentPage" />
    <!-- Fixed navbar -->
    <div class="navbar navbar-default navbar-fixed-top" role="navigation">
      <%include file="header.mako" />
        <div class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li
            % if currentPage == 'home':
              class="active"
            % endif
            ><a href="/home">Home</a></li>
            % if classtype == 'a':
            <li
            % if currentPage == 'manager':
              class="active"
            % endif
             ><a href="/manager">User Manager</a></li>
            <li
            % if currentPage == 'report':
              class="active"
            % endif
             ><a href="/report">Report Generator</a></li>
            <li
            % if currentPage == 'analysis':
              class="active"
            % endif
             ><a href="/analysis">Data Analysis</a></li>
            % endif
            % if classtype == 'r':
            <li
            % if currentPage == 'upload':
              class="active"
            % endif
             ><a href="/upload">Upload Record</a></li>
            % endif
            <li
            % if currentPage == 'search':
              class="active"
            % endif
             ><a href="/search">Search</a></li>
          </ul>
          <ul class="nav navbar-nav navbar-right">
          <li><a href="/doc" target="_blank">Documentation</a></li>
            <li><a href="/user">Logged in as: ${username}</a></li>
            <li
            % if currentPage == 'user':
              class="active"
            % endif
            ><a href="/user">Edit Details</a></li>
            <li><a href="/logout">Logout</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </div>
