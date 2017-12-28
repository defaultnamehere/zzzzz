# 0x01
Install Elasticsearch and Kibana (I'm using 6.0).

# 0x02
Open the browser, go to kibana pannel (default `http://localhost:5601`), go to `DevTools` -> `Console` -> copy and paste from `index.json` click the green arrow. Go back and choose `Management` -> `Index Patters` -> `Create Index Patter` -> choose `elastistalk` (if you didn't change `index.json`).

# 0x03
Run `python fetcherToES.py` and wait for some data.

# 0x04
Go to `Visualize` -> `Create a visualization` -> choose whatever you prefer (`Vertical Bar`) -> choose `elasticstalk` (again, if you didn't change `index.json`) -> `Y-Axis = Count` and `X-Axis, Aggregation = Date Histogram, Field = When` and choose `Interval`. Click the blue arrow.

# 0xtips
If you don't have enough ram and everything stops, in `Visualize` search by name with `print_name:Bill_Gates`.