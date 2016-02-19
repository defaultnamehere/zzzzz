
Stalky
=====

Um hello I guess you're here because you want to look at the code for this or run it yourself. 

The code is up there ^^^^ so I guess here's how you run it yourself.

Installation
-----------

Just run 
```pip install -r requirements.txt```

(virtualenv is for suckers right now)

You'll also need to supply some way of authenticating yourself to Facebook.

Do this by creating the following files:

* `SECRET_UID.txt` - Contains your Facebook user id
* `SECRET_COOKIE.txt` - Contains your Facebook cookie
* `SECRET_CLIENT_ID.txt` - Contains your Facebook client id. Find it by inspecting the GET parameters sent when your browser requests `facebook.com/pull` using your browser's dev tools.


Download some data
------------------

```python fetcher.py```

This will run indefinitely and create data in "log".
Depending on the number of Facebook friends you have, and how active they are, you can expect around 50-100MB/day to be written to disk.

Make some graphs
----------------

1. Run `python graph.py` to convert all the raw log data into CSVs
2. Run `python app.py` to start the 100% CSS-free "webapp"
3. Go to `http://localhost:8000` to view the ultra-minimal "webapp"
4. Paste the Facebook user id that you want to graph into the box.

You did it!

