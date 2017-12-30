# 0x01
Install Elasticsearch and Kibana (I'm using 6.0).

# 0x02
Open the browser, go to Kibana (default `http://localhost:5601`), go to `DevTools` -> `Console` -> copy and paste from `index.json` click the green arrow. Go back and choose `Management` -> `Index Patters` -> `Create Index Pattern` -> choose `elasticstalk` (if you didn't change `index.json`).

# 0x03
Run `python fetcherToES.py` and wait for some data.

# 0x04
Go to `Visualize` -> `Create a visualization` -> choose whatever you prefer (`Vertical Bar`) -> choose `elasticstalk` (again, if you didn't change `index.json`) -> `Y-Axis = Count` and `X-Axis, Aggregation = Date Histogram, Field = When` and choose the `Interval` that you prefer. Click the blue arrow.

# 0xScaling
More than a scaling is a decentralizing and load-balancing, call as you may prefer. The point is that we are going to use Docker. I made a couple of docker containers: `pielco11/zzzzz:original` and `pielco11/zzzzz:es`. The first one is the original repo, to use it do:

1. `docker pull pielco11/zzzzz:original`
2. `docker run -v /full/path/to/SECRETS.txt:/zzzzz/SECRETS.txt` pielco11/zzzzz:original
3. to watch the log: first find the container id of the corresponding image with `docker container ls` and than run `docker logs -f`.

Now the useful stuff. I decided to use the default networking mode (you will see the motivation in the future) so what you will have to do is:

1. `docker pull pielco11/zzzzz:es`;
2. Open `$elasticsearch_home_path/config/elasticsearch.yml` and add `network.host: 127.0.0.1` and `http.host: 0.0.0.0`, so that elasticsearch will expose its APIs over http and let them accessible from "everywhere";
3. Run `ifconfig` and look for `docker`, if you have more `docker` interfaces (`docker1`, `docker2`,...) and don't know what to use just run `docker run --rm -it ubuntu:trusty bash -il` after that `route` and look for `Gateway` (since every container is running, by default, with bridge net mode, the gateway is one, and is your interface that let you communicate with docker containers). It will be likely `172.12.0.1`;
4. Finally run `docker run -v /full/path/to/SECRETS.txt:/zzzzz/SECRETS.txt pielco11/zzzzz:es ip` where ip is the one that you previously found.

# 0xTips
1. If you don't have enough ram and everything stops, in `Visualize` search by name with `print_name:Bill_Gates`.
2. If you have a lot of data to analyze, your pc can crash while creating histograms. So you can try a couple of things, firstly try `line` visualization if this is not enough, instead of `Date Histogram` choose `Date Range` and specify the range. If you have a lot of friends (like many 100s) you can specify more little ranges (otherwise you will run out of ram), so do something like: new range [from: now-1h/h - to now] + new range [from: now-2h/h - to now-1h/h] + ... this will operate in seconds. **Then safe the visualization** so that you don't have to waste your time every once.
