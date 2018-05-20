This directory contains the functional code for running the web server. 

`server.py` is the main server code. It defines the backend behavior of each endpoint. It can be launched by calling `../startserver.sh` from this directory, and it can be shut down by calling `../killserver.sh` from this directory. 

The `templates` directory contains the HTML code because the HTML code utilizes templates to render the page based on the external variable `current_map.txt`.

The `static` directory contains the map files shown on the web page.

As stated above, `current_map.txt` is used to determine which map to use when rendering the HTML. It is written to and read from by `server.py`. 
Note: `current_map.txt` will exist in whichever directory `server.py` was launched from.


