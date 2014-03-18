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
            <li
            % if currentPage == 'search':
              class="active"
            % endif
             ><a href="/search">Search</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </div>